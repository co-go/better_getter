from django.http import HttpResponse
from django.shortcuts import render
from forms import OrderForm
from order import place_order as p_order
from core.login import login_user
import requests

def place_order(request):
    err = None
    valid = None
    if request.method == "POST":
        order_form = OrderForm(request.POST)

        # valid form data, lets generate an order
        if (order_form.is_valid()):
            with requests.Session() as s:
                token = login_user(request.user.wf_email, request.user.wf_password, session=s);
                if (token):
                    item_name = order_form.cleaned_data["item_name"]
                    market_type = request.POST.get("market_type")
                    quantity = order_form.cleaned_data["quantity"]
                    rank = order_form.cleaned_data["rank"]
                    plat = order_form.cleaned_data["plat"]

                    if (p_order(token, item_name, market_type,
                                    item_quantity=quantity, mod_rank=rank,
                                    plat=plat, session=s) == None):

                        err = "There was a problem placing your order, please try again."
                    else:
                        valid = True
                else:
                    err = "We've had a problem logging you in!"

        else:
            err = "Check the values on your form"
    else:
        order_form = OrderForm()

    context = { "order_form": order_form,
                "valid": valid,
                "err": err }

    return render(request, "place_order.html", context)

def get_orders(request, username):
    return username
