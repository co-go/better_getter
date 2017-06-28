from django.http import HttpResponse
from django.shortcuts import render
from forms import OrderForm
from order import place_order as p_order
from core.login import login_user
import requests

def place_order(request):
    err = None
    valid = None
    has_credentials = None
    if request.method == "POST":
        order_form = OrderForm(request.POST)

        # valid form data, lets generate an order
        if (order_form.is_valid()):

            # create a session to use throughout the process
            with requests.Session() as s:
                # log into the user's account, save the token
                token = login_user(request.user.wf_email, request.user.wf_password, session=s);
                if (token):

                    # gather all the form data needed
                    item_name = order_form.cleaned_data["item_name"]
                    market_type = request.POST.get("market_type")
                    quantity = order_form.cleaned_data["quantity"]
                    rank = order_form.cleaned_data["rank"]
                    plat = order_form.cleaned_data["plat"]

                    # try actually placing the order
                    # TODO: in the future, change error message to the actual error
                    if (p_order(token, item_name, market_type,
                                item_quantity=quantity, mod_rank=rank,
                                plat=plat, session=s) == None):

                        err = "There was a problem placing your order, please try again."
                    else:
                        # show valid when the order has successfully been placed
                        valid = True
                else:
                    err = "We've had a problem logging you in!"

        else:
            err = "Check the values on your form"
    else:
        order_form = OrderForm()

    # only users who are logged in should be able to submit stuff
    if (request.user.wf_email != "" and request.user.wf_password != ""):
        has_credentials = True

    context = { "order_form": order_form,
                "valid": valid,
                "err": err,
                "has_credentials": has_credentials }

    return render(request, "place_order.html", context)

def get_orders(request, username):
    return username
