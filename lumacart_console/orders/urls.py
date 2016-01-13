from django.conf.urls import patterns, url
from lumacart_console.orders.views import c2o_send_order

urlpatterns = patterns('',
    url(r'^c2o/send_order/', c2o_send_order),
)