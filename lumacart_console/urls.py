from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'lumacart_console.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^catalogue/', include("lumacart_console.catalogue.urls")),
    url(r'^orders/', include("lumacart_console.orders.urls")),
    url(r'^', include("lumacart_console.dashboard.urls")),
]
