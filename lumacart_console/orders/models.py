from uuid import uuid4

from django.db import models
from lumacart_console.catalogue.models import C2OProduct, C2OSku
from lumacart_console.utils import safe_get

class OrderValidationException(Exception):
    pass

class C2OOrder(models.Model):

    STATUS_NEW = 'NEW'
    STATUS_SENT = 'SENT'
    STATUS_INVALID = 'INVALID'
    STATUS_ERROR = 'ERROR'
    STATUS_DISPATCHED = 'DISPATCHED'
    STATUS_CANCELED = 'CANCELED'

    DELIVERY_STANDARD = 'standard'
    DELIVERY_4DAY = '4day'
    DELIVERY_EXPRESS = 'express'

    luma_id = models.CharField(max_length = 255, blank = False, unique = True)
    c2o_id = models.CharField(max_length = 255, blank = True)
    c2o_status = models.CharField(max_length = 255, blank = True)
    creation_date = models.DateTimeField(blank = False, auto_now_add=True)
    last_update = models.DateTimeField(blank = True, auto_now=True)
    request_json = models.TextField(blank = True)
    response_body = models.TextField(blank = True)
    status = models.CharField(max_length = 30, default = STATUS_NEW, blank = False, choices = [(STATUS_NEW, STATUS_NEW),
                                                                                          (STATUS_SENT, STATUS_SENT),
                                                                                          (STATUS_INVALID, STATUS_INVALID),
                                                                                          (STATUS_ERROR, STATUS_ERROR),
                                                                                          (STATUS_DISPATCHED, STATUS_DISPATCHED) ])
    notes = models.TextField(blank = True)
    delivery_method = models.CharField(max_length = 30, default = DELIVERY_STANDARD, blank = False, choices = [(DELIVERY_STANDARD, DELIVERY_STANDARD),
                                                                                          (DELIVERY_4DAY, DELIVERY_4DAY),
                                                                                          (DELIVERY_EXPRESS, DELIVERY_EXPRESS)])
    individual_bags = models.BooleanField(default = False)
    customer_name	= models.CharField(max_length = 255, blank = False)
    customer_email	= models.CharField(max_length = 255, blank = False)
    customer_telephone	= models.CharField(max_length = 255, blank = True)
    address_delivery_name	= models.CharField(max_length = 255, blank = True)
    address_company_name	= models.CharField(max_length = 255, blank = True)
    address_address_line_1	= models.CharField(max_length = 255, blank = False)
    address_address_line_2	= models.CharField(max_length = 255, blank = True)
    address_city	 = models.CharField(max_length = 255, blank = False)
    address_county	 = models.CharField(max_length = 255, blank = True)
    address_postcode = models.CharField(max_length = 255, blank = False)
    address_country = models.CharField(max_length = 255, blank = False)

    est_dispatch_date = models.DateField(blank = True, null=True)
    net_order_value = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    gross_order_value = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    shipped_by	= models.CharField(max_length = 255, blank = True)
    tracking_link = models.TextField(blank = True)

    store_platform = models.CharField(max_length = 30, blank = True)
    store_order_id = models.CharField(max_length = 255, blank = True)

    def has_issues(self):
        return self.status in [self.STATUS_INVALID, self.STATUS_ERROR] or self.c2o_status in ['On Hold']

    def validate(self):
        for item in self.items.all():
            item.validate()

    @classmethod
    def get_new_luma_id(cls):
        return uuid4()

    def __str__(self):
        return "Order '%s'" % self.luma_id

class C2OOrderItem(models.Model):

    product_id = models.CharField(max_length = 255, blank = False)
    quantity = models.IntegerField(blank = False)
    size = models.CharField(max_length = 20, blank = True)
    order = models.ForeignKey(C2OOrder, related_name="items")
    c2o_sku = models.CharField(max_length = 255, blank = True)

    def validate(self, check_for_send = False):
        product = self.get_product()
        if not product:
            raise OrderValidationException("Can't find product '%s'" % self.product_id)
        if not self.quantity:
            raise OrderValidationException("Empty quantity for %s" % self)
        if not self.size:
            raise OrderValidationException("Empty size for %s" % self)
        sku = safe_get(C2OSku.objects.filter(name = product.sku_name, colour = product.colour, size = self.size))
        if not sku:
            raise OrderValidationException("Can't find sku '%s-%s-%s'" % (product.sku_name, product.colour, self.size))
        self.c2o_sku = sku.sku_code
        self.save()

    def get_product(self):
        return safe_get(C2OProduct.objects.filter(unique_id=self.product_id))

    def __str__(self):
        return "Item '%s'" % self.product_id