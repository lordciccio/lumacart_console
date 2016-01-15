from django.conf.urls import url
from lumacart_console.orders.views import c2o_get_orders

urlpatterns = [
   # url(r'^c2o/send_order/', c2o_send_order),
    url(r'^new_c2o_orders/', c2o_get_orders ),
]