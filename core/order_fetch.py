import requests
import json
from bs4 import BeautifulSoup

ITEMS_URL = "http://warframe.market/api/get_all_items_v2"

def get_item_type(item_name, items):
    """ Will return a dictionary with the item_type and max_rank (if present)

    Args:
        item_name: The name of the item to be found
        items: A JSON object of all the items in the game

    Returns:
        A Dictionary of form:
        {
            "item_type": item_type,
            "max_rank": max_rank
        }
    """
    max_rank = None;
    item_type = None;

    for item in items:
        if (item["item_name"] == item_name):
            # if its a mod, get its 'max_rank'
            if "mod_max_rank" in item.keys():
                max_rank = item["mod_max_rank"]

            # always get the item type
            item_type = item["item_type"]

    return {
                "item_type": item_type,
                "max_rank": max_rank
            }


def filter_items(item, online, ingame):
    """ Appends the item data to the correct type of array

    Args:
        item: JSON formatted object that holds item data
        online: array of parsed items (with sellers that are online)
        ingame: array of parsed items (with sellers that are ingame)

    Returns:
        Nothing. It sets the data into the online and ingame arrays
    """
    seller = item["ingame_name"]

    # we're excluding PS4 and XB1 for now
    if (seller and seller.find("(PS4)") == -1 and seller.find("(XB1)") == -1):

        # build a dict with the item information
        stuffs = {
                    "price": item["price"],
                    "name": seller,
                    "count": item["count"],
                    "mod_rank": item.get("mod_rank")
                }

        # append to the correct array
        if (item["online_ingame"]):
            ingame.append(stuffs)
        elif (item["online_status"]):
            online.append(stuffs)


def item_details(item_name):
    """ Gets the ducat value and picture link for an item

    Args:
        item_name: the name of the item to find

    Returns:
        A dictionary of form:
        {
            "duc": duc,
            "src": src
        }
    """
    r = requests.get("http://warframe.wikia.com/wiki/Ducats/Prices")
    soup = BeautifulSoup(r.text, "html.parser")

    item = item_name.replace("Set", "Blueprint")

    # try and fetch the ducat values
    try:
        duc = soup.find("a", string=item).parent.parent.span.string
    except AttributeError:
        duc = 0

    # try a couple different ways to get an image
    try:
        src = soup.find("a", string=item).previous_sibling.previous_sibling

        if (item_name == "Akbronco Prime Blueprint" or item_name == "Akbronco Prime Link"):
            src = src.img["src"].split("/revision")[0]
        else:
            src = src.img["data-src"].split("/revision")[0]
    except AttributeError:
        try:
            r = requests.get("http://warframe.wikia.com/wiki/" + item)
            soup = BeautifulSoup(r.text, "html.parser")

            src = soup.find("img", class_="pi-image-thumbnail")["src"].split("/revision")[0]
        except:
            src = static("img/notFound.png")

    return {
                "duc": duc,
                "src": src
            }

def get_orders(item_name, item_type):
    """ Function to return the orders for the given item

    Args:
        item_name: the name of the item to get the orders for
        item_type: the type of the item

    Returns:
        A dictionary with all the online, ingame, sell and buy orders
        {
            "ingame_buy": ingame_buy,
            "ingame_sell": ingame_sell,
            "online_buy": online_buy,
            "online_sell": online_sell
        }
    """
    items = requests.get(ITEMS_URL).json()

    # special cases. Maybe move these later?
    if (item_name == "Mesa's Waltz"):
        item_alt_name = "Mesa%E2%80%99s%20Waltz"
        item_type = "Mod"
    elif (item_name == "Paris Prime Lower Limb"):
        item_alt_name = "Paris Prime  Lower Limb"
        item_type = "Blueprint"
    elif (item_name == "Paris Prime Grip"):
        item_alt_name = "Paris Prime  Grip"
        item_type = "Blueprint"
    elif (item_type == None):
        print "[ERR] No item type for item '%s'" % item_name
        return None
    else:
        item_alt_name = item_name

    url = "http://warframe.market/api/get_orders/%s/%s" % ( item_type,
                                                            item_alt_name )
    r = requests.get(url)

    # init our arrays
    current_items = r.json()
    online_sell = []
    ingame_sell = []
    online_buy = []
    ingame_buy = []

    if (current_items["code"] != 404):
        # parse through all of the sell orders
        for item in current_items["response"]["sell"]:
            filter_items(item, online_sell, ingame_sell)

        # and now all of the buy orders
        for item in current_items["response"]["buy"]:
            filter_items(item, online_buy, ingame_buy)

        # lets sort everything
        ingame_buy = sorted(ingame_buy, key=lambda k: k['price'], reverse=True)
        ingame_sell = sorted(ingame_sell, key=lambda k: k['price'])
        online_buy = sorted(online_buy, key=lambda k: k['price'], reverse=True)
        online_sell = sorted(online_sell, key=lambda k: k['price'])
    else:
        print "[ERR] 404, no page found for ITEM: '%s' | TYPE: '%s'"
        return None

    return {
                "ingame_buy": ingame_buy,
                "ingame_sell": ingame_sell,
                "online_buy": online_buy,
                "online_sell": online_sell
            }


def order_handler(item_name):
    """ A Handler that will be called by the /get_item/ pages

    Args:
        item_name: The name of the item to get information for

    Returns:
        A dictionary full of all the information requested
        {
            "item_name": item_name,
            "ducats": item_det["duc"],
            "src": item_det["src"],
            "type": item_info["item_type"],
            "ingame_sell_prices": orders['ingame_sell'][:10],
            "online_sell_prices": orders['online_sell'][:5],
            "ingame_buy_prices": orders['ingame_buy'][:10],
            "online_buy_prices": orders['online_buy'][:5],
            "max_rank": item_info["max_rank"]
        }
    """
    items = requests.get(ITEMS_URL).json()
    item_info = get_item_type(item_name, items)
    orders = get_orders(item_name, item_info["item_type"])

    if (not orders): return None

    item_det = item_details(item_name)

    return {
                "item_name": item_name,
                "ducats": item_det["duc"],
                "src": item_det["src"],
                "type": item_info["item_type"],
                "ingame_sell_prices": orders['ingame_sell'][:10],
                "online_sell_prices": orders['online_sell'][:5],
                "ingame_buy_prices": orders['ingame_buy'][:10],
                "online_buy_prices": orders['online_buy'][:5],
                "max_rank": item_info["max_rank"]
            }
