from django.conf.urls import url
from lumacart_console.hooks.woo.views import new_order

urlpatterns = [
    url(r'^woo/new_order', new_order, name="new_woo_order"),

]