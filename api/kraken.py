import time
import requests
import json
import urllib.parse
import hashlib
from os import path
import hmac
import base64


class Kraken(object):
    api_url_address = "https://api.kraken.com"

    # apikey = "/sk12162sZfc6L7kohoUg7dpPOQfV88ejSwNUpLHvi2UhaX4HwmzT0BX"
    # apisec = "ejLSo7/JmSeBeBW5y33vxJC7QoK/o7yJyYyl9eHyXONJn45Wt/Q639xboW399BJiWf2eiefFuEqQ0qOZ8Pi/mQ=="
    api_key = None    
    api_sec = None

    def get_kraken_signature_from_path(self, urlpath, data):
        post_data = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + post_data).encode()
        msg = urlpath.encode() + hashlib.sha256(encoded).digest()

        mac = hmac.new(base64.b64decode(self.api_sec), msg, hashlib.sha512)
        sig_digest = base64.b64encode(mac.digest())
        return sig_digest.decode()

    def kraken_API_request(self, uri_path, data):
        if not self.api_key:
            return 0

        headers = {}
        headers['API-Key'] = self.api_key
        # get_kraken_signature_from_path() as defined in the 'Authentication' section
        headers['API-Sign'] = self.get_kraken_signature_from_path(uri_path, data)             
        request = requests.post((self.api_url_address + uri_path), headers=headers, data=data)
        print(request.status_code)
        return request

    def place_coin_order(self, volume, pair, buyPrice, orderType = "buy"):
        respond = self.kraken_API_request('/0/private/AddOrder', {
            "nonce": str(int(1000*time.time())),
            "ordertype": "limit",
            "type": orderType,
            "volume": volume,
            "pair": pair,
            "price": buyPrice
        })

        return respond.json()

    def get_coin_balance(self):
        respond = self.kraken_API_request('/0/private/Balance', {"nonce": str(int(1000*time.time()))})

        print(f"[]{self.api_key}[]")
        if not respond:
            return {'code': 404}

        respond = respond.json()
        respond['code'] = 200
        return respond

    def cancel_coin_order(self, order_id_):
        respond = self.kraken_API_request('/0/private/CancelOrder', {
            "nonce": str(int(1000*time.time())),
            "txid": order_id_
        })

        return respond.json()


if __name__ == '__main__':
    krak = Kraken()
    respond = krak.get_coin_balance()
    print(respond)