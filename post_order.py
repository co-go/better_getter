import requests
import json
from bs4 import BeautifulSoup

login_payload = {
    "csrf_token": "",
    "LoginEmail": "USER_EMAIL",
    "LoginPassword": "USER_PASSWORD"
}

order_payload = {
    "item_name": "",
    "item_type": "",
    "action_type": "",
    "item_quantity": 1,
    "platina": 1
}

LOGIN_URL   = "https://warframe.market/signin"
ORDER_URL   = "https://warframe.market/api/place_order"
ITEMS       = None
CSRF_TOKEN  = None

def get_items_json():
    data = requests.get("http://warframe.market/api/get_all_items_v2")
    return data.json()


def main(item_name="Akbronco Prime Blueprint"):
    ITEMS = get_items_json()

    with requests.Session() as s:

        # lets log-in the user
        login_page = s.get(LOGIN_URL)


        soup = BeautifulSoup(login_page.text, 'html.parser')
        CSRF_TOKEN = soup.find(id="csrf_token")['value']

        login_payload['csrf_token'] = CSRF_TOKEN;


        print("[LOGIN] EMAIL: %s | CSRF: %s" % (login_payload['LoginEmail'],
                                                login_payload['csrf_token']));


        # if this request is valid, the session now has an active cookie
        login_post = s.post(
                            LOGIN_URL,
                            data=login_payload,
                            headers={ "Referer": LOGIN_URL }
                            )


        soup = BeautifulSoup(login_post.text, 'html.parser')

        # something went wrong (it cannot find the "Account" dropdown)
        if (soup.find( "a", class_="dropdown-toggle" ) == None):
            print "[ERR] Uh oh! Check your credentials."
            return

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
            return

        print "[ITEM] %s | %s" % (item_name, item_type)

        order_payload["item_name"] = item_name
        order_payload["item_type"] = item_type
        order_payload["action_type"] = "sell"
        order_payload["item_item_namequantity"] = 1
        order_payload["platina"] = 6699

        print("[ORDER] ACTION: %s | QUANTITY: %s | PLAT: %s" % (
            order_payload['action_type'],
            order_payload['item_item_namequantity'],
            order_payload['platina']
            )
        );


        order_post = s.post(
                            ORDER_URL,
                            data=order_payload,
                            headers={
                                    "Referer": ORDER_URL,
                                    "X-CSRFToken": CSRF_TOKEN
                                    }
                            )

        print "[RESPONSE] %s" % order_post.json()['response']

if (__name__ == "__main__"):
    main()
