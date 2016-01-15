import json
import logging
import urllib.request

logger = logging.getLogger("project")

class C2OApi(object):

    def __init__(self, api_key):
        self.api_key = api_key

    def send_order(self, order):
        data = {
            "api_key": self.api_key,
            "order": {
                "order_id": order.luma_id,
                "order_notes": order.notes,
                "delivery_method": order.delivery_method
            },
            "customer": {
                "name": order.customer_name,
                "email":  order.customer_email,
                "telephone": order.customer_telephone
            },
            "address": {
                "delivery_name": order.address_delivery_name,
                "company_name": order.address_company_name,
                "address_line_1": order.address_address_line_1,
                "address_line_2": order.address_address_line_2,
                "city": order.address_city,
                "postcode": order.address_postcode,
                'county': order.address_county,
                "country": order.address_country
            },
            "products": {
                "product": []
            }
        }
        items = []
        for item in order.items.all():
            product = item.get_product()
            item_data = {
                "sku": item.c2o_sku,
                "quantity": "%s" % item.quantity,
                "logos": {
                    "logo": [
                        {
                            "unique_id": product.unique_id,
                            "file": product.file_url,
                            "position": product.print_position,
                            "width": "%s" % product.print_width,
                            "type": product.print_type
                        },
                    ]
                }
            }
            items.append(item_data)
        data['products']['product'] = items

        logger.debug(data)

        req = urllib.request.Request('https://www.clothes2order.com/api/post-order/',
                                     data=json.dumps(data).encode('utf8'),
                                     headers={'Content-Type': 'application/json', 'Accept': 'application/json'})

        response = None
        try:
            response = urllib.request.urlopen(req)
            order.response_body = response

        except Exception as e:
            logger.error(str(e))
            order.status = order.STATUS_ERROR

        order.save()


        return response