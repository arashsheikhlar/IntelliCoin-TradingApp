from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
from pycoingecko import CoinGeckoAPI
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.properties import BooleanProperty

class MainWindow(BoxLayout):
    coins = ListProperty([])
    username = StringProperty("")
    def __init__(self, **kv):
        super().__init__(**kv)
        self.coing = CoinGeckoAPI()
        try:
            self.get_crypto_coins()
        except:
            pass
    
    def get_crypto_coins(self):
        markets = self.coing.get_coins_markets(vs_currency="usd", per_page=50)
        self.coins = markets

        self.ids.home.ids.overviewID.get_watchlist_()
        Clock.schedule_once(self.ids.home.ids.cryptoCurrency.render_, .1)
