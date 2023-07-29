
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.properties import ColorProperty
from kivy.properties import colormap
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.clock import mainthread
from kivy.clock import _get_sleep_obj
from threading import Thread
from threading import setprofile
import json
import os
from widgetsdir.cards import ListTile
from widgetsdir.cards import Asset
from widgetsdir.cards import rgba

Builder.load_file('viewsdir/overview/overview.kv')
class OverviewScrn(BoxLayout):
    coinAssets = ListProperty([])
    balances_ = ListProperty([])
    watchlist = ListProperty([])
    current_cryptoBalance = NumericProperty(0.0)
    def __init__(self, **kv) -> None:
        super().__init__(**kv)
        Clock.schedule_once(self.render_, .2)

    def render_(self, _):
        t1_ = Thread(target=self.get_data_, daemon=True)
        t1_.start()

    @mainthread
    def on_assets_(self, inst, value):
        grid = self.ids.gl_my_assets_ID
        grid.clear_widgets()

        for val in value:
            owned = "".join(["0.0", str(val['symbol']).upper()])

            for bal in self.balances_:
                if bal['cryptoCurrency'] == str(val['symbol']).upper():
                    owned = "%s%s"%(bal['balance'], bal['cryptoCurrency'])
                    break

            ast = Asset()
            ast.height = grid.parent.parent.height*.9
            ast.text = str(val['symbol']).upper()
            ast.source = val['image']
            ast.price = val['current_price']
            ast.data = val
            ast.price_change = val['market_cap_change_percentage_24h']

            ast.owned = owned
            grid.add_widget(ast)

    @mainthread
    def on_watchlist_(self, inst, value):
        grid = self.ids.gl_watchlist_ID
        grid.clear_widgets()

        for val in value:
            ast = ListTile()
            ast.text = str(val['symbol']).upper()
            ast.source = val['image']
            ast.price = val['current_price']
            ast.price_change = val['market_cap_change_percentage_24h']
            ast.data = val
            grid.add_widget(ast)

    def get_data_(self):
        # self.get_watchlist_()
        kraken_data = App.get_running_app().kraken.get_coin_balance()
        okcoin_data = App.get_running_app().okcoin.get_coin_balance()

        all_data = []
        if kraken_data['code'] == 200:
            for k,val in kraken_data['result'].items():
                all_data.append(val)

        if okcoin_data['code'] == 200:
            for o in okcoin_data['result']:
                all_data.append(o)

        self.balances_ = all_data
    
    def on_balances_(self, inst, balances_):
        balances_symbols = [x['cryptoCurrency'] for x in balances_]
        balances_balance = [x['balance'] for x in balances_]
        coins = App.get_running_app().root.coins

        coins = [x for x in coins if x['symbol'].upper() in balances_symbols]
        self.coinAssets = coins
        
        total = 0
        for i, bal in enumerate(balances_balance):
            symbol = balances_symbols[i].lower()
            if symbol == 'usd':
                total += float(bal)
                continue

            tgt_coin = [x for x in coins if x['symbol'] == symbol][0]

            owned = float(bal)*float(tgt_coin['current_price'])
            total += owned
        self.current_cryptoBalance = round(total, 3)

    def refresh_(self):
        App.get_running_app().root.get_crypto_coins()
        t1_ = Thread(target=self.get_data_, daemon=True)
        t1_.start()

    def get_watchlist_(self):
        current_list = {}
        userPath = App.get_running_app().user_data_dir
        savePath = os.path.join(userPath, "watchlist.json")

        if os.path.exists(savePath):
            with open(savePath, "r") as ft:
                current_list = json.load(ft)

        coins = App.get_running_app().root.coins

        coins = [x for x in coins if x['symbol'].upper() in list(current_list.keys())]

        self.watchlist = coins

        

