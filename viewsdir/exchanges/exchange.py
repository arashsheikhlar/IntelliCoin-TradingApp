
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock
import os
import json
from pycoingecko import CoinGeckoAPI

Builder.load_file('viewsdir/exchanges/exchange.kv')
class CoinExchange(BoxLayout):
    coins = ListProperty([])
    def __init__(self, **kv) -> None:
        super().__init__(**kv)
        self.coing = CoinGeckoAPI()

        Clock.schedule_once(self.render_, .2)

    def render_(self, _):
        coinExchanges = [
            {
                "title": "KRAKEN",
                "source": "assets/imgs/kraken_logo.png",
                "require_pass": False,
                "connected": False,
                "keys": {
                    "key":"",
                    "secret": ""
                }
            },
            {
                "title": "OKCOIN",
                "source": "assets/imgs/ok-coin.png",
                "require_pass": True,
                "connected": False,
                "keys": {
                    "key": "",
                    "secret": "",
                    "passphrase": ""
                }
            },
        ]

        keys_ = ['KRAKEN', 'OKCOIN']
        userPath = App.get_running_app().user_data_dir
        savePath = os.path.join(userPath, "keys.json")
        if os.path.exists(savePath):
            data = []

            with open(savePath, "r") as ft:
                allkeys = json.load(ft)

            for k,val in allkeys.items():
                data.append(val)
                if k in keys_:
                    ind = -1
                    for i,e in enumerate(coinExchanges):
                        if e['title'] == k:
                            ind = i
                
                    if ind > -1:
                        coinExchanges.pop(ind)
            
            for e in coinExchanges:
                data.append(e)
            
            coinExchanges = data
            print(coinExchanges)


        grid = self.ids.gl_connected_ID
        exc = self.ids.gl_exchanges_ID
        grid.clear_widgets()
        exc.clear_widgets()

        for e in coinExchanges:
            if e['connected']:
                exch = Connected_Exchanges()
                exch.exchangeTitle = e['title']
                exch.source = e['source']
                exch.connected_ = e['connected']
                exch.require_pass = e['require_pass']
                exch.keys = e['keys']

                grid.add_widget(exch)

            exv = ExchangeTile()
            exv.exchangeTitle = e['title']
            exv.source = e['source']
            exv.connected_ = e['connected']
            exv.require_pass = e['require_pass']
            exv.keys = e['keys']

            exc.add_widget(exv)


class BaseCoinExchange(BoxLayout):
    exchangeTitle = StringProperty("")
    source = StringProperty("")
    connected_ = BooleanProperty(False)
    keys = ObjectProperty(allownone=True)
    require_pass = BooleanProperty(False)
    def __init__(self, **kv) -> None:
        super().__init__(**kv)

class Connected_Exchanges(BaseCoinExchange):
    def __init__(self, **kv) -> None:
        super().__init__(**kv)

class ExchangeTile(BaseCoinExchange):
    def __init__(self, **kv) -> None:
        super().__init__(**kv)

    def get_connect(self):


        newEx = NewExchange()
        newEx.source = self.source
        newEx.exchangeTitle = self.exchangeTitle

        newEx.passphrase_ = self.require_pass
        newEx.open()

class NewExchange(ModalView):
    passphrase_ = BooleanProperty(False)
    source = StringProperty("")
    exchangeTitle = StringProperty("")
    def __init__(self, **kv) -> None:
        super().__init__(**kv)

    def add_exchange_account(self):
        api_key = self.ids.key.text.strip()
        api_secret = self.ids.secret.text.strip()
        password = ""

        if self.passphrase_:
            password = self.ids.password.text.strip()

        if api_key == "" or api_secret == "":
            print("API keys are invalid")
            return

        if self.passphrase_:
            if password == "":
                print("Passphrase is invalid")
                return
        
        data = {
            "title": self.exchangeTitle,
            "source": self.source,
            "connected": True,
            "require_pass": self.passphrase_,
            "keys": {
                "key": api_key,
                "secret": api_secret
            }
        }
        
        if self.passphrase_:
            data['keys']['passphrase'] = password

        userPath = App.get_running_app().user_data_dir
        savePath = os.path.join(userPath, "keys.json")

        if os.path.exists(savePath):
            with open(savePath, "r") as ft:
                allkeys = json.load(ft)
        else:
            allkeys = {}

        allkeys[self.exchangeTitle] = data
        with open(savePath, "w") as ft:
            json.dump(allkeys, ft)

        App.get_running_app().kraken.api_key = api_key
        App.get_running_app().kraken.api_sec = api_secret
        
        self.dismiss()