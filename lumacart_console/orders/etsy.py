import os, sys
import json
from requests_oauthlib import OAuth1Session
import pprint
import django, logging

class EtsyAPI(object):

    def __init__(self, shop_id, client_key, client_secret, resource_owner_key = None, resource_owner_secret = None):
        self.client_key = client_key
        self.client_secret = client_secret
        self.resource_owner_key = resource_owner_key
        self.resource_owner_secret = resource_owner_secret
        self.shop_id = shop_id

    def request_oauth_token(self):
        request_token_url = "https://openapi.etsy.com/v2/oauth/request_token?scope=transactions_r%20transactions_w%20listings_r%20listings_w"
        # Using OAuth1Session
        oauth = OAuth1Session(self.client_key, client_secret=self.client_secret)
        fetch_response = oauth.fetch_request_token(request_token_url)
        print(fetch_response) # open the url!
        resource_owner_key = fetch_response.get('oauth_token')
        resource_owner_secret = fetch_response.get('oauth_token_secret')
        return resource_owner_key, resource_owner_secret

    def obtain_token_credentials(self, temp_resource_owner_key, temp_resource_owner_secret, verifier_from_page):
        access_token_url = 'https://openapi.etsy.com/v2/oauth/access_token'
        # Using OAuth1Session
        oauth = OAuth1Session(self.client_key,
                              client_secret=self.client_secret,
                              resource_owner_key=temp_resource_owner_key,
                              resource_owner_secret=temp_resource_owner_secret,
                              verifier=verifier_from_page)
        oauth_tokens = oauth.fetch_access_token(access_token_url)
        resource_owner_key = oauth_tokens.get('oauth_token')
        resource_owner_secret = oauth_tokens.get('oauth_token_secret')
        return resource_owner_key, resource_owner_secret

    def get_countries(self):
        oauth = OAuth1Session(self.client_key,
                          client_secret=self.client_secret,
                          resource_owner_key=self.resource_owner_key,
                          resource_owner_secret=self.resource_owner_secret)

        r = oauth.get("https://openapi.etsy.com/v2/countries")
        data = json.loads(r.content.decode('utf-8'))
        return data['results']


    def get_new_orders(self):
        oauth = OAuth1Session(self.client_key,
                          client_secret=self.client_secret,
                          resource_owner_key=self.resource_owner_key,
                          resource_owner_secret=self.resource_owner_secret)

        r = oauth.get("https://openapi.etsy.com/v2/shops/%s/receipts/open" % self.shop_id)
        data = json.loads(r.content.decode('utf-8'))
        return data['results']

    def get_order_items(self, receipt_id):
        oauth = OAuth1Session(self.client_key,
                          client_secret=self.client_secret,
                          resource_owner_key=self.resource_owner_key,
                          resource_owner_secret=self.resource_owner_secret)

        r = oauth.get("https://openapi.etsy.com/v2/receipts/%s/transactions" % receipt_id)
        data = json.loads(r.content.decode('utf-8'))
        transactions = data['results']
        items = []
        for t in transactions:
            selected_size_vars = filter(lambda v: v['property_id'] is 100, t['variations'])
            if selected_size_vars:
                r = oauth.get("https://openapi.etsy.com/v2/listings/%s/variations" % t['listing_id'])
                var_data = json.loads(r.content.decode('utf-8'))['results']
                for selected_size_var in selected_size_vars:
                    size_value_id = selected_size_var['value_id']
                    size_variations = list(filter(lambda v: v['property_id'] is 100, var_data))[0]['options']
                    size_info = list(filter(lambda v: v['value_id'] == size_value_id, size_variations))[0]
                    size = size_info['value']
                    item = {
                        'title': t['title'],
                        'listing_id': t['listing_id'],
                        'size': size,
                        'quantity': t['quantity']
                    }
            else:
                size = None
                item = {
                    'title': t['title'],
                    'listing_id': t['listing_id'],
                    'size': size,
                    'quantity': t['quantity']
                }
            items.append(item)
        return items

    def mark_order_as_shipped(self, receipt_id):
        oauth = OAuth1Session(self.client_key,
                          client_secret=self.client_secret,
                          resource_owner_key=self.resource_owner_key,
                          resource_owner_secret=self.resource_owner_secret)
        data = {
            'was_shipped': True
        }
        r = oauth.put("https://openapi.etsy.com/v2/receipts/%s" % receipt_id, data)
        data = json.loads(r.content.decode('utf-8'))


if __name__ == '__main__':
    #how to get ETSY_RESOURCE_OWNER_KEY and ETSY_RESOURCE_OWNER_SECRET:

    os.environ['DJANGO_SETTINGS_MODULE'] = 'lumacart_console.settings'
    django.setup()
    from django.conf import settings
    logger = logging.getLogger("project")

    e = EtsyAPI(settings.ETSY_SHOP_ID, settings.ETSY_CLIENT_KEY, settings.ETSY_CLIENT_SECRET)

    # STEP 1
    #resource_owner_key, resource_owner_secret = e.request_oauth_token()

    # visit the login_url in the prev response, then run following code and replace the verifier code!

    # STEP 2
    #resource_owner_key, resource_owner_secret = e.obtain_token_credentials(resource_owner_key, resource_owner_secret, '....verifier code.....')
    #these one are the permanent ETSY_RESOURCE_OWNER_KEY and ETSY_RESOURCE_OWNER_SECRET

