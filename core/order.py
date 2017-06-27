import requests
from bs4 import BeautifulSoup
import json

ITEM_URL    = "http://warframe.market/api/get_all_items_v2"
ORDER_URL   = "https://warframe.market/api/place_order"
ITEMS       = None

def place_order(session=requests.Session(), item_name, action_type,
                item_quantity=1, plat=default_price(item_name), CSRF_TOKEN):
    """ Attempts to place an order based off of the parameters passed in

    Args:
        session: (Optional) Allows for future GET's using the same session
            to be authenticated. Defaults to arbitrary session if not given.
        item_name: Item name to sell
        action_type: Either "buy" or "sell"
        item_quantity: How many are you selling
        plat: What price is each?
        CSRF_TOKEN: We need this so the server doesn't reject us

    Returns:
        Returns "None" if unable to get the correct information about the item
        or if the order was not submitted. Otherwise a True boolean will be
        returned
    """

    # init the list of all items and their types
    ITEMS = requests.get(ITEM_URL).json()

    # now let's check for the existance of the item
    item_type = None;

    # stupid JSON layout puts item names under "item_name", so we always
    #   have to search through in a loop
    for item in ITEMS:
        if (item["item_name"] == item_name):
            item_type = item["item_type"]
            break

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
