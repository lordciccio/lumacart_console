from django.conf.urls import url
from lumacart_console.dashboard.views import dashboard

urlpatterns = [
    url(r'^$', dashboard),
]