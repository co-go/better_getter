from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from orders.order import order_form_handler
from core.order_fetch import get_public_orders
import requests

@login_required
def place_order(request):
    context = order_form_handler(request)
    return render(request, "place_order.html", context)

def get_orders(request, username):
    context = get_public_orders(username)

    return render(request, "user_orders.html", context)


#http://warframe.market/api/bs_order
#id:59551d4a0f313935ae93bb25
#count:1
