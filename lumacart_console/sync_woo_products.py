#!/usr/bin/env python3.4

import os
import sys
import logging
import django

project_home = u'/home/lumacart/projects/lumacart_console'
if project_home not in sys.path:
    sys.path.append(project_home)

# set environment variable to tell django where your settings.py is
os.environ['DJANGO_SETTINGS_MODULE'] = 'lumacart_console.prod_settings'
django.setup()
logger = logging.getLogger("project")

# add your project directory to the sys.path
from lumacart_console.catalogue.models import C2OProduct, WooVariantSku
from woocommerce import API
from lumacart_console.utils import get_exception_trace, snake_string
from django.conf import settings

try:
    logger.info("Syncing products from WooCommerce...")
    #wcapi = API(
    #    url=settings.WOO_SITE_URL,
    #    consumer_key=settings.WOO_CONSUMER_KEY,
    #    consumer_secret=settings.WOO_CONSUMER_SECRET,
    #    timeout=60
    #)

    #data = wcapi.get("products?filter[limit]=1000")
    #f = open('woo_products.json', 'wt')
    #f.write(data.text)
    #sys.exit(0)
    data = open('woo_products.json', 'rt').read()
    data_json = data.json()
    items = data_json['products']
    logger.info("Found %d items", len(items))
    saved = 0
    for i in items:
        slug_title = snake_string(i['title'])
        product, created = C2OProduct.objects.get_or_create(unique_id=slug_title)
        if created:
            product.sku_name = "Gildan Men's Ring Spun, SoftStyle T-Shirt"
        product.woo_listing_id = i['sku']
        product.title = i['title']
        product.description = i['description']
        product.save()
        product.woo_variants.all().delete()
        for var in i['variations']:
            WooVariantSku.objects.create(product = product, sku = var['sku'])
        saved += 1
    logger.info("Saved %d products", saved)
except:
    err = get_exception_trace()
    logger.error(err)
