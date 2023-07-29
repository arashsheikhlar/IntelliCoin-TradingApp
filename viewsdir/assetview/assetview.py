
import json
import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.metrics import dp, sp
from kivy.properties import ObjectProperty, BooleanProperty, ListProperty, StringProperty, NumericProperty
from kivy.config import Config
from kivy.config import ConfigParser
from kivy.garden.graph import LinePlot
from kivy.garden.iconfonts import icon
from kivy.clock import Clock

Builder.load_file('viewsdir/assetview/assetview.kv')
class AssetView(ModalView):
    cryptoCurrency = StringProperty("BTC")
    cryptoAsset_value = NumericProperty(42342.62)
    source = StringProperty("")
    chart_data = ListProperty([0,1])
    one_day_data = ListProperty([0,1])
    one_week_data = ListProperty([0,1])
    one_month_data = ListProperty([0,1])
    one_year_data = ListProperty([0,1])
    data = ObjectProperty(allownone=True)
    def __init__(self, **kv) -> None:
        super().__init__(**kv)
        self.alert = Alert()
        Clock.schedule_once(self.render_, .2)

    def render_(self, _):
        graph = self.ids.asset_graph_ID
        plot = LinePlot()
        plot.line_width = dp(1.2)
        plot.color = App.get_running_app().colors.thirdlevel_light

        self.ids.asset_graph_ID.add_plot(plot)

    def on_data(self, inst, data):

        self.ids.market_cap_ID.text = str(data['market_cap'])
        self.ids.low_ID.text = str(data['low_24h'])
        self.ids.volume_ID.text = str(data['total_volume'])
        self.ids.high_ID.text = str(data['high_24h'])
        self.ids.circulating_supply_ID.text = str(data['circulating_supply'])
        self.ids.total_supply_ID.text = str(data['total_supply'])

        price_change_amount = str(data['price_change_percentage_24h'])[:4] + "%"
        price_change_signed = price_change_amount.replace("+-", "-")
        self.ids.price_change.text = price_change_signed

    def update_graph(self, data_type="day"):
        if data_type == 'hour':
            target_data = [x for x in self.one_day_data[-60:]]
        if data_type == 'day':
            target_data = self.one_day_data
        elif data_type == 'week':
            target_data = self.one_week_data
            print(target_data)
        elif data_type == 'month':
            target_data = self.one_month_data
        elif data_type == 'year':
            target_data = self.one_year_data

        if len(target_data) > 4:
            self.chart_data = target_data

    def on_chart_data(self, inst, coinPrices):
        graph = self.ids.asset_graph_ID
        plots = graph.plots


        if len(plots) == 0:
            return

        points = []
        ymax = 0
        ymin = min(coinPrices)

        for i, p in enumerate(coinPrices):
            pt = (i+1, p)
            points.append(pt)

            if p > ymax:
                ymax = p

        graph.ymax = ymax
        graph.ymin = ymin
        plots[0].points = points

    def place_coin_order(self, buy=True):
        balances_ = self.get_coin_balance()

        ao = AssetOrder()
        ao.buy = buy
        ao.cryptoAsset_value = self.cryptoAsset_value
        ao.cryptoCurrency = self.cryptoCurrency
        ao.current_cryptoBalance = float(balances_['usd']) if buy else float(balances_[self.cryptoCurrency])
        ao.open()

    def get_coin_balance(self) -> dict:
        home = App.get_running_app().root.ids.home
        overviewID = home.ids.overviewID

        usd_balance = overviewID.current_cryptoBalance
        balances_ = overviewID.balances_
        owned = 0

        for bal in balances_:
            if bal['cryptoCurrency'] == self.cryptoCurrency.upper():
                owned = bal['balance']
                break
        currency_balance = owned
        return {'usd': usd_balance, self.cryptoCurrency: currency_balance}

    def watch(self):
        homeID = App.get_running_app().root.ids.home
        overviewID = homeID.ids.overviewID
        current_list = {}

        userPath = App.get_running_app().user_data_dir
        savePath = os.path.join(userPath, "watchlist.json")
        if os.path.exists(savePath):
            with open(savePath, "r") as ft:
                current_list = json.load(ft)
        if not self.cryptoCurrency in list(current_list.keys()):
            current_list[self.cryptoCurrency] = True

        with open(savePath, "w") as ft:
            json.dump(current_list, ft)

        self.alert.text = f"{self.cryptoCurrency} Added to watchlist"
        self.alert.open()

        overviewID.get_watchlist_()

class AssetOrder(ModalView):
    buy = BooleanProperty(True)
    cryptoCurrency = StringProperty("BTC")
    cryptoAsset_value = NumericProperty(0.0)
    current_cryptoBalance = NumericProperty(0.0)
    current_cryptoOrder = StringProperty("0.00")
    def __init__(self, **kv) -> None:
        super().__init__(**kv)
        Clock.schedule_once(self.render_, .2)

    def render_(self, _):
        keys_ = '789456123.0-'
        numpad = self.ids.numpad
        numpad.clear_widgets()

        for ky in keys_:
            anchor = AnchorLayout()
            kyp = KeyPad()
            if ky == "-":
                ky = icon("icon-delete")
                kyp.filled = False
                kyp.bind(on_release=self.backspace)
            else:
                kyp.bind(on_release=self.key_press)

            if ky == ".":
                kyp.filled = False
            kyp.text = str(ky)

            anchor.add_widget(kyp)
            numpad.add_widget(anchor)

    def place_coin_order(self, okcoin=True):
        buyPrice = str(self.cryptoAsset_value)
        pair = "%s-USD"%self.cryptoCurrency.upper()
        volume = str(self.current_cryptoOrder)

        orderType = "buy" if self.buy else "sell"
        if okcoin:
            App.get_running_app().okcoin.place_coin_order(volume, pair, buyPrice, orderType=orderType)
        else:
            App.get_running_app().kraken.place_coin_order(volume, pair, buyPrice, orderType=orderType)

    def key_press(self, inst):
        if self.current_cryptoOrder == "0.00":
            self.current_cryptoOrder = ""
        self.current_cryptoOrder += str(inst.text)

    def backspace(self, inst):
        self.current_cryptoOrder = self.current_cryptoOrder[:-1]
        if self.current_cryptoOrder == "":
            self.current_cryptoOrder = "0.00"

class KeyPad(Button):
    filled = BooleanProperty(True)
    def __init__(self, **kv) -> None:
        super().__init__(**kv)

class Alert(ModalView):
    text = StringProperty("")
    def __init__(self, **kv) -> None:
        super().__init__(**kv)

        self.bind(on_open=self.close)

    def close(self, *args):
        Clock.schedule_once(self.dismiss, 2)
