import logging
from django.shortcuts import render
from django.conf import settings
from lumacart_console.orders.c2o_api import C2OApi
from lumacart_console.orders.models import C2OOrder, OrderValidationException

logger = logging.getLogger("project")

def c2o_get_new_orders(request, message = None):
    orders = C2OOrder.objects.filter(status__in = [C2OOrder.STATUS_NEW, C2OOrder.STATUS_INVALID]).order_by('-creation_date')
    params = {'orders': orders, 'message': message}
    return render(request, "orders.html", params)

def _perform_order_validation(order):
    error = None
    try:
        order.validate()
        order.status = C2OOrder.STATUS_NEW
    except OrderValidationException as e:
        error = e.args[0]
        order.status = C2OOrder.STATUS_INVALID
    order.save()
    return error

def c2o_check_order(request):
    order_id = request.POST.get('id')
    order = C2OOrder.objects.get(id = order_id)
    error = _perform_order_validation(order)
    return c2o_get_new_orders(request, message = error)

def c2o_send_order(request):
    order_id = request.POST.get('id')
    order = C2OOrder.objects.get(id = order_id)
    error = _perform_order_validation(order)
    if order.status != order.STATUS_NEW:
        error = "Order is not NEW"
    if not error:
        api = C2OApi(settings.C2O_API_KEY)
        api.send_order(order)
    return c2o_get_new_orders(request, message = error)