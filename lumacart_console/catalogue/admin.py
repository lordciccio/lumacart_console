
from django.contrib import admin
from lumacart_console.catalogue.models import C2OProduct



class C2OProductAdmin(admin.ModelAdmin):
    list_display = ['unique_id', 'description', 'print_width', 'print_type']
    search_fields = ['unique_id', 'description']
    list_filter = ['print_width', 'print_type']


admin.site.register(C2OProduct, C2OProductAdmin)