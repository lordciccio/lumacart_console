from django import forms
from django.contrib import admin
from lumacart_console.catalogue import models
from lumacart_console.catalogue.models import C2OProduct, C2OSku

def get_sorted_sku_names_choices():
    return models.C2OSku.objects.all().order_by('name').values_list('name', 'name').distinct()

def get_sorted_colour_choices(sku_name):
    return models.C2OSku.objects.filter(name=sku_name).order_by('colour').values_list('colour', 'colour').distinct()


class C2OSkuAdmin(admin.ModelAdmin):
    list_display = ['sku_code', 'name', 'category', 'in_stock', 'colour', 'size']
    search_fields = ['sku_code', 'name']
    list_filter = ['in_stock', 'colour', 'category', 'size']

    def img_preview(self, obj):
        return '<img src="%s" width="120"/>' % (obj.file_url)
    img_preview.allow_tags = True


admin.site.register(C2OSku, C2OSkuAdmin)

class C2OProductAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super(C2OProductAdminForm, self).__init__(*args, **kwargs)
        self.fields['sku_name'] = forms.ChoiceField(required = True, choices=get_sorted_sku_names_choices())
        colour_choices = []
        if instance:
            colour_choices = get_sorted_colour_choices(instance.sku_name)
        self.fields['colour'] = forms.ChoiceField(required = False, choices=colour_choices)

    class Meta:
        model = C2OProduct
        fields = '__all__'


class C2OProductAdmin(admin.ModelAdmin):
    list_display = ['unique_id', 'title', 'colour', 'print_width', 'img_preview']
    search_fields = ['unique_id', 'description']
    list_filter = ['colour', 'print_width', 'print_type']
    form = C2OProductAdminForm

    def img_preview(self, obj):
        return '<img src="%s" width="120"/>' % (obj.file_url)
    img_preview.allow_tags = True


admin.site.register(C2OProduct, C2OProductAdmin)