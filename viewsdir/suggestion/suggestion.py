from kivy.app import App
from kivy.lang import Builder
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.clock import mainthread
import numpy as np
from kivy.properties import ListProperty
from kivy.core.window import Window
from pycoingecko import CoinGeckoAPI

from widgetsdir.cards import Asset2
import time

Builder.load_file('viewsdir/suggestion/suggestion.kv')


class Suggestion(BoxLayout):
    coins = ListProperty([])
    popular = ListProperty(['btc', 'eth', 'doge', 'ltc', 'dash', 'ada', 'xmr', 'bnb', 'xrp', 'usdt', 'bch'])

    def __init__(self, **kv) -> None:
        super().__init__(**kv)
        self.coing = CoinGeckoAPI()

        Clock.schedule_once(self.render_, .2)

    def render_(self, _):
        self.coins = App.get_running_app().root.coins

    def refresh_(self):
        App.get_running_app().root.get_crypto_coins()
        self.coins = App.get_running_app().root.coins

    @mainthread
    def on_coins(self, inst, markets):
        popular = self.ids.gl_popular
        popular.clear_widgets()



        for val in markets:
            if str(val['symbol']) in self.popular:
                ast = Asset2()
                ast.text = str(val['symbol']).upper()
                ast.source = val['image']
                ast.price = round(val['current_price'], 2)
                ast.price_change = val['market_cap_change_percentage_24h']
                ast.data = val
                ast.height = Window.height * .2
                popular.add_widget(ast)

                # Linear regression calculations
                lm = LinearRegression()
                x = np.arange(1, len(ast.daily_prices) + 1).reshape(-1, 1)
                y = ast.daily_prices
                lm.fit(x, y)
                slope = lm.coef_

                if slope * ast.price_change > 0.1:
                    ast.suggest = str("BUY")
                else:
                    ast.suggest = str("NoAction")