import json
import logging
import pycountry
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse
from django.http.response import HttpResponseServerError
from lumacart_console.catalogue.models import C2OProduct
from lumacart_console.orders.models import C2OOrderItem, C2OOrder
from lumacart_console.orders.routines import send_admin_email, convert_to_c2o_size
from lumacart_console.utils import get_exception_trace, blank_if_none, safe_get

logger = logging.getLogger("project")

def new_order(request):
    logger.info("Receiving new order from woocommerce...")
    data = json.loads(request.body.decode())
    o = data["order"]
    logger.info(" -> order is: %s - %s (%s)", o["order_number"], o["order_key"], o["created_at"])
    try:
        with transaction.atomic():
            order, created = C2OOrder.objects.get_or_create(store_platform = 'woo', store_order_id = o["order_key"])
            if created:
                logger.info("found new order with woo key id '%s', saving...", o["order_key"])
                order.luma_id = C2OOrder.get_new_luma_id()
                order.notes = blank_if_none(o.get('note', ''))
                cust = o['customer']
                addr = o.get("shipping_address", {})
                order.customer_name	= cust['first_name'] + " " + cust['last_name']
                order.customer_email = cust.get("email", "")
                order.customer_telephone =  o['customer'].get("billing_address", {}).get("phone", "")
                order.address_delivery_name	= addr['first_name'] + " " + addr['last_name']
                order.address_company_name = addr.get('company', '')
                order.address_address_line_1 = blank_if_none(addr.get('address_1', ''))
                order.address_address_line_2 = blank_if_none(addr.get('address_2', ''))
                order.address_city = blank_if_none(addr.get('city', ''))
                order.address_county = blank_if_none(addr.get('state', ''))
                order.address_postcode = blank_if_none(addr.get('postcode', ''))
                country = pycountry.countries.get(alpha2=addr.get('country', ''))
                order.address_country = country.name
                order.save()
                link = settings.HOST + '/orders/new_c2o_orders/'
                for item in o['line_items']:
                    product = safe_get(C2OProduct.objects.filter(woo_variants__sku = item['sku']))
                    if not product:
                        logger.warning("Can't find a WooCommerce product for %s, title: '%s' - listing_id: '%s'" % (order, item['name'], item['sku']))
                        send_admin_email("Order #%s - product missing!" % order.luma_id, "Can't find a WooCommerce product for order #%s, title: '%s' - listing_id: '%s'" % (order.luma_id, item['name'], item['sku']))
                        continue
                    size_info = safe_get(list(filter(lambda m: m['key'] == 'pa_size', item['meta'])))
                    if not size_info:
                        raise Exception("Can't find size meta in WooCommerce order item! (%s - %s)" % (item['name'], item['sku']))
                    size = size_info['value']
                    C2OOrderItem.objects.create(order = order,
                                                product_id = product.unique_id,
                                                size = convert_to_c2o_size(size),
                                                quantity = item['quantity'])
                send_admin_email("New order from WooCommerce", "Your new WooCommerce order can be found here: %s" % link)
            else:
                logger.warning("order with woo key '%s' already exists!", o["order_key"])
                send_admin_email("Order duplicated from WooCommerce", "Order with woo key '%s' already exists!" % o["order_key"])
    except:
        logger.error(get_exception_trace())
        return HttpResponseServerError()
    return HttpResponse("ok!")
