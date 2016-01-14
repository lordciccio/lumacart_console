import tempfile
import logging
from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from lumacart_console.utils import safe_get
from lumacart_console.utils.readers import get_reader
from lumacart_console.catalogue import models

logger = logging.getLogger("project")

def handle_uploaded_file(f):
    temp = tempfile.NamedTemporaryFile(delete = False)
    with open(temp.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return temp.name

class ImportForm(forms.Form):
    file = forms.FileField()

C2O_CATEGORIES = ['T-Shirts', 'Aprons', 'Bags']

@login_required
def import_c2o_catalogue(request):
    params = {}
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file_path = handle_uploaded_file(request.FILES['file'])
            csv_reader = get_reader('CSV')()
            csv_reader.parse_doc(open(uploaded_file_path, encoding='utf-8'))
            models.C2OSku.objects.all().delete()
            saved = 0
            for record in csv_reader.iter_doc():
                sku = safe_get(models.C2OSku.objects.filter(sku_code = record['SKU']))
                if not sku:
                    sku = models.C2OSku(sku_code = record['SKU'])
                sku.name = record['Product Name']
                sku.category = record['Product Category']
                sku.colour = record['Colour']
                sku.in_stock = int(record['In Stock'])
                sku.size = record['Size']
                if sku.category in C2O_CATEGORIES:
                    sku.save()
                    saved += 1
                logger.info("saved sku '%s'" % sku.sku_code)
            params['saved'] = str(saved)
    else:
        form = ImportForm()
    params['form'] = form
    return render(request, "import.html", params)