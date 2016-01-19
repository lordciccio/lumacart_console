#!/usr/bin/env python3.4

import os
import sys
import logging
import django
from lumacart_console.utils import get_exception_trace

project_home = u'/home/lumacart/projects/lumacart_console'
if project_home not in sys.path:
    sys.path.append(project_home)

# set environment variable to tell django where your settings.py is
os.environ['DJANGO_SETTINGS_MODULE'] = 'lumacart_console.prod_settings'
django.setup()
logger = logging.getLogger("project")

# add your project directory to the sys.path
from lumacart_console.orders.routines import update_order_status, check_for_new_etsy_orders, send_admin_email
from lumacart_console.orders.models import C2OOrder

try:
    logger.info("Checking orders status...")
    for order in C2OOrder.objects.filter(status__in = [C2OOrder.STATUS_SENT]):
        update_order_status(order)

    logger.info("Fetching new Etsy orders...")
    check_for_new_etsy_orders()
except:
    err = get_exception_trace()
    logger.error(err)
    send_admin_email("update_orders script error", err)