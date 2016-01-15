from django.shortcuts import render
from lumacart_console.orders.models import C2OOrder, C2OOrderItem


def c2o_get_orders(request):
    status = request.GET.get('status', C2OOrder.STATUS_NEW)
    orders = C2OOrder.objects.filter(status = status).order_by('-creation_date')
    params = {'orders': orders}
    return render(request, "orders.html", params)