from django.http import HttpResponse
from django.shortcuts import render

import requests
import json
from bs4 import BeautifulSoup

import logging
logger = logging.getLogger(__name__)

def get_item_details(request, item_name):
    # grab the latest item data and parse it
    data = requests.get("http://warframe.market/api/get_all_items_v2")
    items = data.json()

    # function that returns the type of the item (if it exists)
    def ret_type(item_n):
        for item in items:
            if (item["item_name"] == item_n):
                return item["item_type"]

    # return a connection to the orders for the passed in item
    def connect(item_n, item_t=ret_type(item_name)):
        url = "http://warframe.market/api/get_orders/%s/%s" % (item_t, item_n)
        r = requests.get(url)
        return r

    if (item_name == "Mesa's Waltz"):
        r = connect("Mesa%E2%80%99s%20Waltz", "Mod")
    elif (item_name == "Paris Prime Lower Limb"):
        r = connect("Paris Prime  Lower Limb", "Blueprint")
    else:
        r = connect(item_name)

    current_items = r.json()
    online_sell_prices = []
    ingame_sell_prices = []
    online_buy_prices = []
    ingame_buy_prices = []

    mr = None

    if (current_items["code"] != 404):
        for item in current_items["response"]["sell"]:
            if (mr == None):
                mr = "mod_rank" in item.keys()

            if (item["online_ingame"] and
                item["ingame_name"].find("(PS4)") == -1 and
                item["ingame_name"].find("(XB1)") == -1):

                if (mr):
                    ingame_sell_prices.append({"price": item["price"],
                                               "name": item["ingame_name"],
                                               "count": item["count"],
                                               "mod_rank": item["mod_rank"]})
                else:
                    ingame_sell_prices.append({"price": item["price"],
                                               "name": item["ingame_name"],
                                               "count": item["count"]})

            elif (item["online_status"] and
                  item["ingame_name"].find("(PS4)") == -1 and
                  item["ingame_name"].find("(XB1)") == -1):

                if (mr):
                    online_sell_prices.append({"price": item["price"],
                                               "name": item["ingame_name"],
                                               "count": item["count"],
                                               "mod_rank": item["mod_rank"]})
                else:
                    online_sell_prices.append({"price": item["price"],
                                               "name": item["ingame_name"],
                                               "count": item["count"]})

        for item in current_items["response"]["buy"]:
            if (item["online_ingame"] and
                item["ingame_name"].find("(PS4)") == -1 and
                item["ingame_name"].find("(XB1)") == -1):

                if (mr):
                    ingame_buy_prices.append({"price": item["price"],
                                               "name": item["ingame_name"],
                                               "count": item["count"],
                                               "mod_rank": item["mod_rank"]})
                else:
                    ingame_buy_prices.append({"price": item["price"],
                                               "name": item["ingame_name"],
                                               "count": item["count"]})

            elif (item["online_status"] and
                  item["ingame_name"].find("(PS4)") == -1 and
                  item["ingame_name"].find("(XB1)") == -1):

                if (mr):
                    online_buy_prices.append({"price": item["price"],
                                              "name": item["ingame_name"],
                                              "count": item["count"],
                                              "mod_rank": item["mod_rank"]})
                else:
                    online_buy_prices.append({"price": item["price"],
                                               "name": item["ingame_name"],
                                               "count": item["count"]})


        ingame_buy_prices = sorted(ingame_buy_prices, key=lambda k: k['price'], reverse=True)
        ingame_sell_prices = sorted(ingame_sell_prices, key=lambda k: k['price'])
        online_buy_prices = sorted(online_buy_prices, key=lambda k: k['price'], reverse=True)
        online_sell_prices = sorted(online_sell_prices, key=lambda k: k['price'])

        r = requests.get("http://warframe.wikia.com/wiki/Ducats/Prices")
        soup = BeautifulSoup(r.text, "html.parser")

        item = item_name.replace("Set", "Blueprint")

        try:
            duc = soup.find("a", string=item).parent.parent.span.string
        except AttributeError:
            duc = "N/A"

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
                src = "/static/img/notFound.png"


        context = { "item_name": item_name,
                    "ducats": duc,
                    "src": src,
                    "type": ret_type(item_name),
                    "ingame_sell_prices": ingame_sell_prices[:10],
                    "online_sell_prices": online_sell_prices[:5],
                    "ingame_buy_prices": ingame_buy_prices[:10],
                    "online_buy_prices": online_buy_prices[:5] }
    else:
        context = { "err": True }

    return render(request, 'get_item/item.html', context)
