import requests
from bs4 import BeautifulSoup
import json
from core.primary_orders import get_orders, get_item_type

ITEM_URL    = "http://warframe.market/api/get_all_items_v2"
ORDER_URL   = "https://warframe.market/api/place_order"
ITEMS       = None


def default_price(item_name, action_type):
    item_info = get_item_type(item_name)
    orders = get_orders(item_name, item_info["item_type"])

    if (not orders): return -69

    try:
        price = orders["ingame_" + action_type][0]
    except IndexError:
        try:
            price = orders["online_" + action_type][0]
        except IndexError:
            price = -69

    if (action_type == "sell" and price != -69):
        price -= 1
    else:
        price += 1

    return price


def place_order(CSRF_TOKEN, item_name, action_type, item_quantity=1,
                plat=None, session=requests.Session()):
    """ Attempts to place an order based off of the parameters passed in

    Args:
        CSRF_TOKEN: We need this so the server doesn't reject us
        item_name: Item name to sell
        action_type: Either "buy" or "sell"
        item_quantity: How many are you selling
        plat: (Optional) What price is each item? If not provided, will default
            to the best price based on if sell/buy +- 1.
        session: (Optional) Allows for future GET's using the same session
            to be authenticated. Defaults to arbitrary session if not given.

    Returns:
        Returns "None" if unable to get the correct information about the item
        or if the order was not submitted. Otherwise a True boolean will be
        returned
    """

    # no plat value was given, lets try to make one
    if (plat == None):
        plat = default_price(item_name, action_type)

        if (plat == -69):
            print "[ERR] Could not get an accurate price, user must provide one."
            return None

    # init the list of all items and their types
    ITEMS = requests.get(ITEM_URL).json()

    # now let's check for the existance of the item
    item_type = None;

    # stupid JSON layout puts item names under "item_name", so we always
    #   have to search through in a loop
    item_type = get_item_type(item_name)["item_type"]

    # couldn't find it, return
    if (item_type == None):
        print "[ERR] There was a problem finding the type of '%s'" % item_name
        return None

    # we have the item and its type, lets generate an order
    print "[ITEM] %s | %s" % (item_name, item_type)

    order_payload = {
        "item_name": item_name,
        "item_type": item_type,
        "action_type": action_type,
        "item_quantity": item_quantity,
        "platina": plat
    }

    print("[ORDER] ACTION: %s | QUANTITY: %s | PLAT: %s" % (
        order_payload['action_type'],
        order_payload['item_item_namequantity'],
        order_payload['platina']
        )
    );

    # submit the order
    order_post = session.post(
                              ORDER_URL,
                              data=order_payload,
                              headers={
                                       "Referer": ORDER_URL,
                                       "X-CSRFToken": CSRF_TOKEN
                                       }
                              )

    # we were able to submit the order, lets check it
    print "[RESPONSE] %s" % order_post.json()['response']

    return True
