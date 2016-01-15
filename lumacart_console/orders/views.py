import logging
from django.shortcuts import render
from django.conf import settings
from lumacart_console.orders.c2o_api import C2OApi
from lumacart_console.orders.models import C2OOrder, OrderValidationException

logger = logging.getLogger("project")

def c2o_get_new_orders(request, messages = {}):
    orders = C2OOrder.objects.filter(status__in = [C2OOrder.STATUS_NEW, C2OOrder.STATUS_INVALID, C2OOrder.STATUS_ERROR]).order_by('-creation_date')
    params = {'orders': orders, 'messages': messages}
    return render(request, "orders.html", params)

def _perform_order_validation(order):
    error = None
    success = True
    try:
        order.validate()
        order.status = C2OOrder.STATUS_NEW
    except OrderValidationException as e:
        error = e.args[0]
        order.status = C2OOrder.STATUS_INVALID
        success = False
    order.save()
    return success, error

def c2o_check_order(request):
    order_id = request.POST.get('id')
    order = C2OOrder.objects.get(id = order_id)
    success, output = _perform_order_validation(order)
    messages = {}
    if not success:
        messages = {
            'danger': [output]
        }
    return c2o_get_new_orders(request, messages = messages)

def c2o_send_order(request):
    order_id = request.POST.get('id')
    order = C2OOrder.objects.get(id = order_id)
    success, output = _perform_order_validation(order)
    if not success:
        messages = {
            'danger': [output]
        }
    else:
        if order.status != order.STATUS_NEW:
            messages = {
                'danger': ["Order is not NEW"]
            }
        else:
            api = C2OApi(settings.C2O_API_KEY)
            success, messages = api.send_order(order)
    messages = {
        'success' if success else 'danger': messages
    }
    return c2o_get_new_orders(request, messages = messages)