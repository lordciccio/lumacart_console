import json
import logging
import urllib.request
from datetime import datetime
from urllib.error import HTTPError
from lumacart_console.utils import get_exception_trace

logger = logging.getLogger("project")

class C2OApi(object):

    def __init__(self, api_key):
        self.api_key = api_key

    def _process_send_response(self, order, body):
        order.response_body = body
        response = json.loads(body.decode('utf8'))
        if response['status']['code'] == 'OK':
            order.status = order.STATUS_SENT
            order.c2o_id = response['order_details']['order_id']
            order.est_dispatch_date = datetime.strptime(response['order_details']['est_dispatch_date'], "%d/%m/%Y")
            order.net_order_value = response['order_details']['net_order_value']
            order.gross_order_value = response['order_details']['gross_order_value']
            messages = ["Sent %s: %s" % (order, response['status']['msg'])]
        else:
            order.status = order.STATUS_ERROR
            messages = [response['status']['msg']]
        if 'warnings' in response:
            warnings = response['warnings'].get('warning', [])
            messages.extend(warnings)
        order.save()
        return messages

    def _process_fetch_response(self, order, body):
        order.response_body = body
        response = json.loads(body.decode('utf8'))
        if response['status']['code'] == 'OK':
            order.est_dispatch_date = datetime.strptime(response['order_details']['est_dispatch_date'], "%d/%m/%Y")
            order.net_order_value = response['order_details']['net_order_value']
            order.gross_order_value = response['order_details']['gross_order_value']
            order.c2o_status = response['order_details']['order_status']
            order.shipped_by = response['order_details']['shipped_by']
            order.tracking_link = response['order_details']['tracking_link']
            order.save()
        messages = [response['status']['msg']]
        return messages

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

        try:
            logger.debug(data)
            json_data = json.dumps(data)
            order.request_json = json_data
            order.save()
            req = urllib.request.Request('https://www.clothes2order.com/api/post-order/',
                                         data=json_data.encode('utf8'),
                                         headers={'Content-Type': 'application/json', 'Accept': 'application/json'})

            response = urllib.request.urlopen(req)
            order.response_body = response.read()
            logger.debug(order.response_body)
            messages = self._process_send_response(order, order.response_body)
            return True, messages
        except HTTPError as he:
            error = he.read()
            if he.code == 400:
                messages = self._process_send_response(order, error)
            else:
                messages = [error]
                logger.error(error)
        except Exception as e:
            logger.error(get_exception_trace())
            messages = [str(e)]

        logger.error('messages:\n%s' % messages)
        order.status = order.STATUS_ERROR
        order.save()
        return False, messages

    def check_order_status(self, order):
        data = {
            "api_key": self.api_key,
            "order": {
                "your_order_id": order.luma_id
            }
        }
        try:
            logger.debug(data)
            json_data = json.dumps(data)
            req = urllib.request.Request('https://www.clothes2order.com/api/fetch-order/',
                                         data=json_data.encode('utf8'),
                                         headers={'Content-Type': 'application/json', 'Accept': 'application/json'})

            response = urllib.request.urlopen(req)
            order.response_body = response.read()
            logger.debug(order.response_body)
            messages = self._process_fetch_response(order, order.response_body)
            return True, messages
        except HTTPError as he:
            error = he.read()
            logger.error(error)
            messages = [error]
        except Exception as e:
            logger.error(get_exception_trace())
            messages = [str(e)]
        return False, messages