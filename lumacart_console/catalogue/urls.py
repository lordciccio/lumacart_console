from django.conf.urls import url
from lumacart_console.catalogue.views import import_c2o_catalogue


urlpatterns =[
     url(r'^import_c2o/', import_c2o_catalogue),
]