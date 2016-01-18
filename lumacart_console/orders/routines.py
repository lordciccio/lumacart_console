import logging
from django.conf import settings
from lumacart_console.orders.c2o_api import C2OApi
from lumacart_console.orders.models import C2OOrder
logger = logging.getLogger("project")

def update_order_status(order):
    logger.info("checking status for %s...", order)
    api = C2OApi(settings.C2O_API_KEY)
    success, messages = api.check_order_status(order)
    if success:
        if order.c2o_status == 'Dispatched':
            order.status = C2OOrder.STATUS_DISPATCHED
            order.save()
        logger.info("order c2o status: %s", order.c2o_status)
    else:
        logger.info("could not fetch status: %s", '\n'.join(messages))
