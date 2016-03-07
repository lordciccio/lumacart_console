import logging
from django.http import HttpResponse

logger = logging.getLogger("project")

def new_order(request):
    logger.info("GET:")
    logger.info(request.GET)
    logger.info("POST:")
    logger.info(request.POST)
    logger.info("META:")
    logger.info(request.META)
    logger.info("body:")
    logger.info(request.body)
    return HttpResponse("ok")
