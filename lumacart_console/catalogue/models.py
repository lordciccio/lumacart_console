
from django.db import models

C2O_POSITIONS = [
    ("1" ,"Right Sleeve (max 10 cm)"),
    ("2" , "Bottom Right (max 12 cm)"),
    ("3" , "Right Chest	 (max 12 cm)"),
    ("4" , "Centre Chest (max 30 cm)"),
    ("5" , "Left Chest	(max 12 cm)"),
    ("6" , "Bottom Left	(max 12 cm)"),
    ("7" , "Left Sleeve	(max 10 cm)"),
    ("8" , "Centre Back	(max 30 cm)"),
    ("9" , "Top Back (max 30 cm)"),
    ("11", "Front of Hat (max 8 cm)"),
    ("12", "Bottom Back	(max 30 cm)"),
    ("13", "Front of Bag (max 30 cm)"),
    ("14", "Centre Tea Towel (max 30 cm)"),
    ("15", "Left Pocket	(max 12 cm)"),
    ("16", "Right Pocket (max 12 cm)"),
    ("17", "Top Chest (max 30 cm)"),
    ("18", "Inside Back (max 12 cm)"),
    ("19", "Front of Tie (max 5 cm)")
]

C2O_PRINT_TYPE_PRINT = 'print'
C2O_PRINT_TYPE_PRINT_1 = 'print_1colour'
C2O_PRINT_TYPE_EMBROIDERY = 'embroidery'

class C2OSku(models.Model):
    key = models.CharField(max_length = 255, blank = False, primary_key=True)
    category = models.CharField(max_length = 255, blank = True)
    name = models.CharField(max_length = 255, blank = False)
    in_stock = models.BooleanField()
    sku_code = models.CharField(max_length = 255, blank = False)
    colour = models.CharField(max_length = 255, blank = False)
    size = models.CharField(max_length = 255, blank = False)

    def save(self, **kwargs):
        self.key = "%s-%s-%s" % (self.name, self.colour, self.size)
        super(C2OSku, self).save(**kwargs)

    def __str__(self):
         return "C2O Sku '%s'" % self.key

class C2OProduct(models.Model):

    unique_id = models.CharField(max_length = 255, blank = False, unique = True)
    sku_name = models.CharField(max_length = 255, blank = True)
    title = models.CharField(max_length = 255, blank = False)
    description = models.TextField(blank = True)
    file_url = models.TextField(blank = True)
    print_position = models.CharField(max_length = 30, default = "4", blank = False, choices = C2O_POSITIONS)
    print_width = models.IntegerField(blank = False, default = 30)
    print_type = models.CharField(max_length = 30, default = C2O_PRINT_TYPE_PRINT, blank = False, choices = [(C2O_PRINT_TYPE_PRINT, 'Print multi-colour'),
                                                                                                   (C2O_PRINT_TYPE_PRINT_1, "Single-color print"),
                                                                                                   (C2O_PRINT_TYPE_EMBROIDERY, "Embroidery")])
    colour = models.CharField(max_length = 255, blank = True)
    etsy_listing_id = models.CharField(max_length = 255, blank = True)
    woo_listing_id = models.CharField(max_length = 255, blank = True)

    def __str__(self):
         return "C2O Product '%s'" % self.unique_id


class WooVariantSku(models.Model):
    product = models.ForeignKey("C2OProduct", related_name="woo_variants")
    sku = models.CharField(max_length = 255, blank = False)
