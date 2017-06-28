from django.http import HttpResponse
from django.shortcuts import render
from core.primary_orders import order_handler

import logging
logger = logging.getLogger(__name__)

def get_item_details(request, item_name):
    context = order_handler(item_name) or { "err": True }

    return render(request, 'item.html', context)
