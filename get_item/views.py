from django.http import HttpResponse
from django.shortcuts import render
from orders.order import order_form_handler
from core.order_fetch import order_handler
import requests

import logging
logger = logging.getLogger(__name__)

def get_item_details(request, item_name):
    context = order_handler(item_name)
    if (not context):
         context.update({ "main_err": True })
    else:
        context.update({ "main_err": False })
        context.update(order_form_handler(request, item_name=item_name))

    return render(request, 'item.html', context)
