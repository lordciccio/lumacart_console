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
os.environ['C2O_API_KEY'] = '6NHMoQYdOHbjBIZEwNe4cliHQ50fGHNNvvzUmy7afjtR1svxgKCs6V9W1abHRZvn'

django.setup()
logger = logging.getLogger("project")

# add your project directory to the sys.path
from lumacart_console.orders.routines import update_order_status
from lumacart_console.orders.models import C2OOrder

logger.info("Checking orders status...")
for order in C2OOrder.objects.filter(status__in = [C2OOrder.STATUS_SENT]):
    update_order_status(order)
