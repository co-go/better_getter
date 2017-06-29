from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from orders.order import order_form_handler
from core.order_fetch import get_public_orders, get_private_orders
from core.login import login_user
import requests

@login_required
def place_order(request):
    context = order_form_handler(request)
    return render(request, "place_order.html", context)

def get_user_orders(request, username):
    context = get_public_orders(username)

    return render(request, "user_orders.html", context)

@login_required
def get_orders(request):
    user = request.user
    err = None
    with requests.Session() as s:
        if (user.wf_email and user.wf_password):
            # attempt to log in the user
            token = login_user(user.wf_email, user.wf_password, s)
            if (token):
                # get ourselves some orders
                context = get_private_orders(s)
            else:
                err = "There was a problem logging you in!"
        else:
            err = "Please enter in your warframe.market credentials."

    context.update({"err": err})

    return render(request, "orders.html", context)

#http://warframe.market/api/bs_order
#id:59551d4a0f313935ae93bb25
#count:1
