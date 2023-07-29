import os
import json
import datetime
import sys
import requests
import base64
import hmac

CONTENT_T = 'Content-Type'
OK_ACCESS_K = 'OK-ACCESS-KEY'
OK_ACCESS_S = 'OK-ACCESS-SIGN'
OK_ACCESS_T = 'OK-ACCESS-TIMESTAMP'
OK_ACCESS_P = 'OK-ACCESS-PASSPHRASE'
app_J = 'app/json'
GET = 'GET'
POST = 'POST'

class OKcoin(object):

    api_url_address = "https://www.okcoin.com"
    api_key = None
    api_sec = None
    pass_phrase = None
    # apikey = "2b8248a6-3dfb-4f40-b44f-cfa32f18e195"
    # apisec = "66072F864FC529751ED9A0BA9049067E"
    # pass_phrase = "#hash537/OK"

    def get_okcoin_signature_from_path(self, t, method, pathRequest, body=None):

        if str(body) == '{}' or str(body) == 'None' or body == None:
            body = ''
        msg = str(t) + str.upper(method) + pathRequest + str(body)
        mac = hmac.new(bytes(self.api_sec, encoding='utf8'), bytes(msg, encoding='utf-8'), digestmod='sha256')
        dep = mac.digest()
        return base64.b64encode(dep)

    def get_header_(self, sig, t):
        header = dict()
        header[CONTENT_T] = app_J
        header[OK_ACCESS_K] = self.api_key
        header[OK_ACCESS_S] = sig
        header[OK_ACCESS_T] = t
        header[OK_ACCESS_P] = self.pass_phrase
        return header

    def okcoin_API_request(self, type, pathRequest, body=''):
        if not self.api_key:
            return
        if type == "GET":
            if body != '':
                url = '?'
                for key, value in body.items():
                    url = url + str(key) + '=' + str(value) + '&'

                body = url[0:-1]
        elif type == 'POST':
            body = json.dumps(body)
            print("NEWB: ", body)

        timestamp_ = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "Z"
        signature = self.get_okcoin_signature_from_path(timestamp_, type, pathRequest, body)
        header = self.get_header_(signature, timestamp_)

        # do request
        if type == 'GET':
            response = requests.get(self.api_url_address + pathRequest + body,
                    headers=header)
        else:
            print(self.api_url_address + pathRequest)
            response = requests.post(self.api_url_address + pathRequest, data_=body,
                    headers=header)

        return response

    def place_coin_order(self, volume, pair, buyPrice, orderType="buy"):

        print("Placing an order...")
        respond = self.okcoin_API_request(POST, '/api/spot/v3/orders', {
            "type": "limit", 
            "side": orderType, 
            "instrument_id": pair, 
            "size": volume, 
            "price": buyPrice})
        
        data_ = json.loads(respond.content)
        print(data_)

        if data_['error_code'] == '0':
            if os.path.exists("orders.json"):
                with open("orders.json", "r") as ft:
                    orders = json.load(ft)
            else:
                orders = {}

            orders[data_['order_id_']] = {"pair": pair}
            with open("orders.json", "w") as ft:
                json.dump(orders, ft)

        print("Order was placed...")
        return data_

    def get_instruments(self):
        respond = self.okcoin_API_request(GET, "/api/spot/v3/instruments")

        return json.loads(respond.content)

    def get_coin_balance(self):

        print("Getting coin balance...")
        respond = self.okcoin_API_request(GET, "/api/spot/v3/accounts")

        if not respond:
            return {"code": 404}
        
        data_ = {"result": json.loads(respond.content)}
        data_['code'] = 200
        
        return data_

    def cancel_coin_order(self, order_id_):

        if os.path.exists("orders.json"):
                with open("orders.json", "r") as ft:
                    orders = json.load(ft)
        else:
            return {'error_code': 100, "message": "Failed to fetch the orders"}

        instrument_id = orders[order_id_]['pair']
        respond = self.okcoin_API_request(POST,'/api/spot/v3/cancel_orders/'+order_id_, {
            "order_id_": order_id_,
            "instrument_id": instrument_id
        })

        data_ = json.loads(respond.content)
        if data_['result'] == True:
            orders.pop(order_id_)
            with open("orders.json", "w") as ft:
                json.dump(orders, ft)

        return data_


if __name__ == '__main__':
    okC = OKcoin()
    respond = okC.get_coin_balance()
    print("="*60)
    print(respond) 