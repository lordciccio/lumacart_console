from uuid import uuid4
from django import forms
from django.contrib import admin
from django.contrib.admin.options import TabularInline
from lumacart_console.catalogue import models
from lumacart_console.orders.models import C2OOrder, C2OOrderItem

def get_sorted_product_choices():
    return models.C2OProduct.objects.all().order_by('title').values_list('unique_id', 'title')

def get_sorted_sizes(product = None):
    qs = models.C2OSku.objects.all().order_by('size').values_list('size', 'size').distinct()
    if product:
        qs = qs.filter(name = product.sku_name)
    return [('', '')] + list(qs)

class C2OOrderItemInlineForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super(C2OOrderItemInlineForm, self).__init__(*args, **kwargs)
        self.fields['product_id'] = forms.ChoiceField(required = True, choices=get_sorted_product_choices())
        product = None
        if instance:
            product = instance.get_product()
        self.fields['size'] = forms.ChoiceField(required = False, choices=get_sorted_sizes(product))

    class Meta:
        model = C2OOrderItem
        fields = '__all__'

class C2OOrderItemInline(TabularInline):
    model = C2OOrderItem
    extra = 0
    form = C2OOrderItemInlineForm
    readonly_fields = ('c2o_sku',)

class C2OOrdeForm(forms.ModelForm):

    def save(self, *args, **kwargs):
        self.instance.luma_id = uuid4()
        return super(C2OOrdeForm, self).save(*args, **kwargs)

    class Meta:
        model = C2OOrder
        fields = '__all__'

class C2OOrderAdmin(admin.ModelAdmin):
    list_display = ['luma_id', 'c2o_id', 'creation_date', 'status', 'est_dispatch_date', 'gross_order_value']
    search_fields = ['luma_id', 'c2o_id']
    list_filter = ['status']
    inlines = [C2OOrderItemInline]
    form = C2OOrdeForm
    exclude = ['luma_id']
    readonly_fields = ['c2o_id', 'request_json', 'response_body', 'est_dispatch_date', 'net_order_value', 'gross_order_value']

admin.site.register(C2OOrder, C2OOrderAdmin)