from django.shortcuts import render_to_response
from django.template.context import RequestContext


def import_c2o_catalogue(request):
    params = {}
    
    return render_to_response("catalogue.html", context_instance=RequestContext(request, params))