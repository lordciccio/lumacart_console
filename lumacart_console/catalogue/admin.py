
from django.contrib import admin
from lumacart_console.catalogue.models import C2OProduct, C2OSku


class C2OSkuAdmin(admin.ModelAdmin):
    list_display = ['sku_code', 'name', 'category', 'in_stock', 'colour', 'size']
    search_fields = ['sku_code', 'name']
    list_filter = ['in_stock', 'colour', 'category', 'size']

    def img_preview(self, obj):
        return '<img src="%s" width="120"/>' % (obj.file_url)
    img_preview.allow_tags = True


admin.site.register(C2OSku, C2OSkuAdmin)

class C2OProductAdmin(admin.ModelAdmin):
    list_display = ['unique_id', 'title', 'colour', 'print_width', 'img_preview']
    search_fields = ['unique_id', 'description']
    list_filter = ['colour', 'print_width', 'print_type']

    def img_preview(self, obj):
        return '<img src="%s" width="120"/>' % (obj.file_url)
    img_preview.allow_tags = True


admin.site.register(C2OProduct, C2OProductAdmin)