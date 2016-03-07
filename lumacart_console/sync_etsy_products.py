#!/usr/bin/env python3.4

import os
import sys
import logging
import django
import html.parser

project_home = u'/home/lumacart/projects/lumacart_console'
if project_home not in sys.path:
    sys.path.append(project_home)

# set environment variable to tell django where your settings.py is
os.environ['DJANGO_SETTINGS_MODULE'] = 'lumacart_console.prod_settings'
django.setup()
logger = logging.getLogger("project")

# add your project directory to the sys.path
from lumacart_console.catalogue.models import C2OProduct
from lumacart_console.orders.etsy import EtsyAPI
from lumacart_console.utils import get_exception_trace, snake_string
from django.conf import settings

try:
    logger.info("Syncing products from Etsy...")
    etsy = EtsyAPI(settings.ETSY_SHOP_ID, settings.ETSY_CLIENT_KEY, settings.ETSY_CLIENT_SECRET, settings.ETSY_RESOURCE_OWNER_KEY, settings.ETSY_RESOURCE_OWNER_SECRET)
    items = etsy.get_shop_active_items()
    logger.info("Found %d items", len(items))
    saved = 0
    for i in items:
        title = html.unescape(i['title'])
        slug_title = snake_string(title)
        product, created = C2OProduct.objects.get_or_create(unique_id=slug_title)
        if created:
            product.sku_name = "Gildan Men's Ring Spun, SoftStyle T-Shirt"
        product.etsy_listing_id = i['listing_id']
        product.title = title
        product.description = i['description']
        product.save()
        saved += 1
    logger.info("Saved %d products", saved)
except:
    err = get_exception_trace()
    logger.error(err)
