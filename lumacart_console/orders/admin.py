from django import forms
from django.contrib import admin
from django.contrib.admin.options import TabularInline
from lumacart_console.orders.models import C2OOrder, C2OOrderItem

class C2OOrderItemInlineForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(C2OOrderItemInlineForm, self).__init__(*args, **kwargs)
        self.fields['product_id'] = forms.ChoiceField(required = True, choices=[ (o, str(o)) for o in ['', 'b', 'c']])

    class Meta:
        model = C2OOrderItem
        fields = '__all__'

class C2OOrderItemInline(TabularInline):
    model = C2OOrderItem
    extra = 0
    form = C2OOrderItemInlineForm

class C2OOrderAdmin(admin.ModelAdmin):
    list_display = ['luma_id', 'c2o_id', 'creation_date', 'status', 'last_update']
    search_fields = ['luma_id', 'c2o_id']
    list_filter = ['status']
    inlines = [C2OOrderItemInline]

admin.site.register(C2OOrder, C2OOrderAdmin)