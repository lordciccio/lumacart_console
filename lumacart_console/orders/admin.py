from uuid import uuid4
from django import forms
from django.contrib import admin
from django.contrib.admin.options import TabularInline
from lumacart_console.orders.models import C2OOrder, C2OOrderItem

def get_sorted_product_choices():
    from lumacart_console.catalogue import models
    return models.C2OProduct.objects.all().order_by('title').values_list('unique_id', 'title')

class C2OOrderItemInlineForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(C2OOrderItemInlineForm, self).__init__(*args, **kwargs)
        self.fields['product_id'] = forms.ChoiceField(required = True, choices=get_sorted_product_choices())

    class Meta:
        model = C2OOrderItem
        fields = '__all__'

class C2OOrderItemInline(TabularInline):
    model = C2OOrderItem
    extra = 0
    form = C2OOrderItemInlineForm


class C2OOrdeForm(forms.ModelForm):

    def save(self, *args, **kwargs):
        self.instance.luma_id = uuid4()
        return super(C2OOrdeForm, self).save(*args, **kwargs)

    class Meta:
        model = C2OOrder
        fields = '__all__'

class C2OOrderAdmin(admin.ModelAdmin):
    list_display = ['luma_id', 'c2o_id', 'creation_date', 'status', 'last_update']
    search_fields = ['luma_id', 'c2o_id']
    list_filter = ['status']
    inlines = [C2OOrderItemInline]
    form = C2OOrdeForm
    exclude = ['luma_id']

admin.site.register(C2OOrder, C2OOrderAdmin)