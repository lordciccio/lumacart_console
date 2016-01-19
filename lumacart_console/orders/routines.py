import logging
import pprint
from django.conf import settings
from django.core.mail import send_mail
from lumacart_console.orders.c2o_api import C2OApi
from lumacart_console.orders.models import C2OOrder
from lumacart_console.orders.etsy import EtsyAPI
from lumacart_console.utils import get_exception_trace

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
                send_admin_email("Order #%s dispatched" % order.luma_id, "C2O service has dispatched order #%s" % order.luma_id)
                order.save()

                if order.store_platform == 'etsy':
                    logger.info("marking Etsy order status as shipped...")
                    etsy = EtsyAPI(settings.ETSY_SHOP_ID, settings.ETSY_CLIENT_KEY, settings.ETSY_CLIENT_SECRET, settings.ETSY_RESOURCE_OWNER_KEY, settings.ETSY_RESOURCE_OWNER_SECRET)
                    etsy.mark_order_as_shipped(order.store_order_id)

            except:
                logger.error("Can't update order dispatch status: %s", get_exception_trace())
    else:
        logger.info("could not fetch status: %s", '\n'.join(messages))


def check_for_new_etsy_orders():
    logger.info("searching etsy orders with status 'open'...")
    etsy = EtsyAPI(settings.ETSY_SHOP_ID, settings.ETSY_CLIENT_KEY, settings.ETSY_CLIENT_SECRET, settings.ETSY_RESOURCE_OWNER_KEY, settings.ETSY_RESOURCE_OWNER_SECRET)
    countries = etsy.get_countries()
    orders = etsy.get_new_orders()
    for o in orders:
        receipt_id = o['receipt_id']
        country = list(filter(lambda c: c['country_id'] == o['country_id'], countries))[0]
        order, created = C2OOrder.objects.get_or_create(store_platform = 'etsy', store_order_id = receipt_id)
        if created:
            logger.info("found new order with etsy id '%s', saving...", receipt_id)
            pprint.pprint(etsy.get_order_items(receipt_id))
            order.luma_id = C2OOrder.get_new_luma_id()
            order.notes = o['message_from_buyer']
            order.customer_name	= o['name']
            order.customer_email = o['buyer_email']
            order.customer_telephone = ''
            order.address_delivery_name	= o['name']
            order.address_company_name = ''
            order.address_address_line_1 = o['first_line']
            order.address_address_line_2 = o['second_line']
            order.address_city = o['city']
            order.address_county = o['state']
            order.address_postcode = o['zip']
            order.address_country = country['name']
            order.save()
            link = settings.HOST + '/orders/new_c2o_orders/'
            send_admin_email("New order from Etsy", "Your new Etsy order can be found here: %s" % link)
