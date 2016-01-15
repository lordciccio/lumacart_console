from django.conf.urls import url
from lumacart_console.orders.views import c2o_get_new_orders, c2o_check_order, c2o_send_order

urlpatterns = [
    url(r'^new_c2o_orders/', c2o_get_new_orders, name="new_c2o_orders"),
    url(r'^check_c2o_order/', c2o_check_order, name="check_c2o_order" ),
    url(r'^send_c2o_order/', c2o_send_order, name="send_c2o_order" ),
]