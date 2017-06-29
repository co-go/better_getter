from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from orders.order import order_form_handler
import requests

@login_required
def place_order(request):
    context = order_form_handler(request)
    return render(request, "place_order.html", context)

def get_orders(request, username):
    return username
