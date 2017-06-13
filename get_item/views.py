from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.staticfiles.templatetags.staticfiles import static

import requests
import json
from bs4 import BeautifulSoup

import logging
logger = logging.getLogger(__name__)

def get_item_details(request, item_name):
    # grab the latest item data and parse it
    data = requests.get("http://warframe.market/api/get_all_items_v2")
    items = data.json()

    max_rank = None;
    item_type = None;

    # return a connection to the orders for the passed in item
    def connect(item_n, item_t):
        url = "http://warframe.market/api/get_orders/%s/%s" % (item_t, item_n)
        r = requests.get(url)
        return r


    for item in items:
        if (item["item_name"] == item_name):

            if "mod_max_rank" in item.keys():
                max_rank = item["mod_max_rank"]

            item_type = item["item_type"]


    if (item_name == "Mesa's Waltz"):
        item_type = "Mod"
        r = connect("Mesa%E2%80%99s%20Waltz", item_type)
    elif (item_name == "Paris Prime Lower Limb"):
        item_type = "Blueprint"
        r = connect("Paris Prime  Lower Limb", item_type)
    elif (item_name == "Paris Prime Grip"):
        item_type = "Blueprint"
        r = connect("Paris Prime  Grip", item_type)
    elif (item_type == None):
        return render(request, 'get_item/item.html', {'err: True'})
    else:
        r = connect(item_name, item_type)

    current_items = r.json()
    online_sell_prices = []
    ingame_sell_prices = []
    online_buy_prices = []
    ingame_buy_prices = []

    if (current_items["code"] != 404):
        for item in current_items["response"]["sell"]:

            if (item["online_ingame"] and
                item["ingame_name"].find("(PS4)") == -1 and
                item["ingame_name"].find("(XB1)") == -1):

                if (max_rank != None):
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

                if (max_rank != None):
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

                if (max_rank != None):
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

                if (max_rank != None):
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
            duc = 0

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


        context = { "item_name": item_name,
                    "ducats": duc,
                    "src": src,
                    "type": item_type,
                    "ingame_sell_prices": ingame_sell_prices[:10],
                    "online_sell_prices": online_sell_prices[:5],
                    "ingame_buy_prices": ingame_buy_prices[:10],
                    "online_buy_prices": online_buy_prices[:5],
                    "max_rank": max_rank }
    else:
        context = { "err": True }

    return render(request, 'get_item/item.html', context)
