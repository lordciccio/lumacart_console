import logging
import pprint
from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction

from lumacart_console.orders.c2o_api import C2OApi
from lumacart_console.orders.models import C2OOrder, C2OOrderItem
from lumacart_console.orders.etsy import EtsyAPI
from lumacart_console.utils import get_exception_trace, safe_get, blank_if_none
from lumacart_console.catalogue.models import C2OProduct

logger = logging.getLogger("project")

def send_admin_email(subj, text):
    try:
        send_mail(settings.EMAIL_SUBJECT_PREFIX + subj, text, settings.EMAIL_SENDER,
            [settings.ADMIN_EMAIL], fail_silently=False)
    except Exception as e:
        logger.error(get_exception_trace())

def update_order_status(order):
    logger.info("checking status for %s...", order)
    api = C2OApi(settings.C2O_API_KEY)
    success, messages = api.check_order_status(order)
    if success:
        if order.c2o_status == 'Dispatched':
            try:
                order.status = C2OOrder.STATUS_DISPATCHED
                logger.info("%s c2o status is now %s!", order, order.c2o_status)
                send_admin_email("Order #%s dispatched" % order.luma_id, "C2O service has dispatched order #%s.\nTracking link is: %s" % (order.luma_id, order.tracking_link))
                order.save()

                if order.store_platform == 'etsy':
                    logger.info("marking Etsy order status as shipped...")
                    etsy = EtsyAPI(settings.ETSY_SHOP_ID, settings.ETSY_CLIENT_KEY, settings.ETSY_CLIENT_SECRET, settings.ETSY_RESOURCE_OWNER_KEY, settings.ETSY_RESOURCE_OWNER_SECRET)
                    etsy.mark_order_as_shipped(order.store_order_id)

            except:
                logger.error("Can't update order dispatch status: %s", get_exception_trace())
    else:
        logger.info("could not fetch status: %s", '\n'.join(messages))


def convert_to_c2o_size(size):
    c = {
        'small': 'S',
        'medium': 'M',
        'large': 'L',
        'x-large': 'XL',
        '2x-large': 'XXL',
        '3/4 years (xs)': 'XS',
        '5/6 years (s)': 'S',
        '7/8 years (m)': 'M',
        '9/11 years (l)': 'L',
        '12/14 years (xl)': 'XL'
    }
    return c.get(size.lower(), size)

def check_for_new_etsy_orders():
    logger.info("searching etsy orders with status 'open'...")
    etsy = EtsyAPI(settings.ETSY_SHOP_ID, settings.ETSY_CLIENT_KEY, settings.ETSY_CLIENT_SECRET, settings.ETSY_RESOURCE_OWNER_KEY, settings.ETSY_RESOURCE_OWNER_SECRET)
    countries = etsy.get_countries()
    orders = etsy.get_new_orders()
    for o in orders:
        receipt_id = o['receipt_id']
        country = list(filter(lambda c: c['country_id'] == o['country_id'], countries))[0]
        with transaction.atomic():
            order, created = C2OOrder.objects.get_or_create(store_platform = 'etsy', store_order_id = receipt_id)
            if created:
                logger.info("found new order with etsy id '%s', saving...", receipt_id)
                order.luma_id = C2OOrder.get_new_luma_id()
                order.notes = blank_if_none(o.get('message_from_buyer', ''))
                order.customer_name	= o['name']
                order.customer_email = o['buyer_email']
                order.customer_telephone = ''
                order.address_delivery_name	= o['name']
                order.address_company_name = ''
                order.address_address_line_1 = blank_if_none(o.get('first_line', ''))
                order.address_address_line_2 = blank_if_none(o.get('second_line', ''))
                order.address_city = blank_if_none(o.get('city', ''))
                order.address_county = blank_if_none(o.get('state', ''))
                order.address_postcode = blank_if_none(o.get('zip', ''))
                order.address_country = country['name']
                order.save()
                link = settings.HOST + '/orders/new_c2o_orders/'
                for item in etsy.get_order_items(receipt_id):
                    product = safe_get(C2OProduct.objects.filter(etsy_listing_id = item['listing_id']))
                    if not product:
                        logger.warning("Can't find an Etsy product for %s, title: '%s' - listing_id: '%s'" % (order, item['title'], item['listing_id']))
                        send_admin_email("Order #%s - product missing!" % order.luma_id, "Can't find an Etsy product for order #%s, title: '%s' - listing_id: '%s'" % (order.luma_id, item['title'], item['listing_id']))
                        continue
                    C2OOrderItem.objects.create(order = order,
                                                product_id = product.unique_id,
                                                size = convert_to_c2o_size(item['size']),
                                                quantity = item['quantity'])
                send_admin_email("New order from Etsy", "Your new Etsy order can be found here: %s" % link)
            else:
                if order.status == C2OOrder.STATUS_NEW:
                    logger.warning("new order with etsy id '%s' already exists!", receipt_id)
                    send_admin_email("New Order duplicated from Etsy", "Order with etsy id '%s' already exists!" % receipt_id)