from django.http import HttpResponse
from django.shortcuts import render

import requests
import json
from bs4 import BeautifulSoup

def index(request):
    return HttpResponse("<h1> Item could not be found! </h1>")

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
    def connect(item_n):
        r = requests.get("http://warframe.market/api/get_orders/%s/%s" % (ret_type(item_n), item_n))
        return r

    r = connect(item_name)

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

                ingame_sell_prices.append({"price": item["price"], "name": item["ingame_name"], "count": item["count"]})

            elif (item["online_status"] and
                  item["ingame_name"].find("(PS4)") == -1 and
                  item["ingame_name"].find("(XB1)") == -1):

                online_sell_prices.append({"price": item["price"], "name": item["ingame_name"], "count": item["count"]})

        for item in current_items["response"]["buy"]:
            if (item["online_ingame"] and
                item["ingame_name"].find("(PS4)") == -1 and
                item["ingame_name"].find("(XB1)") == -1):

                ingame_buy_prices.append({"price": item["price"], "name": item["ingame_name"], "count": item["count"]})

            elif (item["online_status"] and
                  item["ingame_name"].find("(PS4)") == -1 and
                  item["ingame_name"].find("(XB1)") == -1):

                online_buy_prices.append({"price": item["price"], "name": item["ingame_name"], "count": item["count"]})

        ingame_buy_prices = sorted(ingame_buy_prices, key=lambda k: k['price'], reverse=True)
        ingame_sell_prices = sorted(ingame_sell_prices, key=lambda k: k['price'])
        online_buy_prices = sorted(online_buy_prices, key=lambda k: k['price'], reverse=True)
        online_sell_prices = sorted(online_sell_prices, key=lambda k: k['price'])

        r = requests.get("http://warframe.wikia.com/wiki/Ducats/Prices")
        soup = BeautifulSoup(r.text, "html.parser")

        item = item_name.replace("Set", "Blueprint")

        duc = soup.find("a", string=item).parent.parent.span.string
        src = soup.find("a", string=item).previous_sibling.previous_sibling

        if (item_name == "Akbronco Prime Blueprint" or item_name == "Akbronco Prime Link"):
            src = src.img["src"].split("/revision")[0]
        else:
            src = src.img["data-src"].split("/revision")[0]

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
