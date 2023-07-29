
from threading import Thread
from kivy.app import App
from kivy.lang import Builder
from viewsdir.assetview import AssetView

from sklearn.linear_model import LinearRegression
import numpy as np
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, ListProperty
from kivy.clock import Clock
from kivy.clock import mainthread
from kivy.metrics import dp
from kivy.utils import rgba
import json
from kivy.garden.graph import LinePlot
import requests
from pycoingecko import CoinGeckoAPI
import time


Builder.load_string("""

<Asset2>:
    size_hint: [None, None]
    width: Window.size[0]*.85
    height: dp(240)
    orientation: 'vertical'
    spacing: dp(8)
    padding: dp(4)
    halign: "center"
    canvas.before:
        Color:
            rgba: app.colors.subordinate
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(16)]
    BoxLayout:
        size_hint_y: None
        height: dp(42)
        AnchorLayout:
            size_hint_x: None
            width: dp(54)
            BoxLayout:
                size_hint: [None, None]
                size: [dp(42), dp(42)]
                padding: dp(4)
                RelativeLayout:
                    AsyncImage:
                        id: imgproxy
                        source: root.source
                        opacity: 0
                    Widget:
                        canvas.before:
                            Color:
                                rgba: [1,1,1,1]
                            Ellipse:
                                size: self.size[0], self.size[1]
                                pos: self.pos
                                texture: imgproxy.texture
        
        BoxLayout:
            size_hint_x: .3
            Text:
                text: root.text
                font_name: app.fonts.headingfont
                color: app.colors.white
                font_size: app.fonts.size.s5                        
    BoxLayout:
        Graph:
            id: graph
            draw_border: False      
    BoxLayout:
        size_hint_y: None
        height: dp(62)
        orientation: "vertical" 
        BoxLayout:
            orientation: "horizontal"
            Text:
                text: "Value:"
                font_name: app.fonts.bodyfont
                font_size: app.fonts.size.s6
                color: app.colors.white
                valign: "top"
                halign: "center"
            Text:
                text: "$%s"%str(root.price)
                font_name: app.fonts.headingfont
                color: app.colors.white
                valign: "top"
                halign: "center"
        BoxLayout:
            orientation: "horizontal"
            Text:
                text: "Price change:"
                font_name: app.fonts.bodyfont
                font_size: app.fonts.size.s6
                color: app.colors.white
                valign: "top"
                halign: "center"
            Text:
                id: price_change
                font_name: app.fonts.headingfont
                color: app.colors.Emerald_Green
                valign: "top"
                halign: "center"        
        BoxLayout:
            orientation: "horizontal"
            Text:
                text: "AI Suggestion:"
                font_name: app.fonts.bodyfont
                font_size: app.fonts.size.s6                                        
                color: app.colors.white
                valign: "top"
                halign: "center"
            Text:
                id: suggest
                font_name: app.fonts.headingfont
                color: app.colors.Emerald_Green
                valign: "top"
                halign: "center"          
                   
""")

class Card(ButtonBehavior, BoxLayout):
    source = StringProperty("")
    text = StringProperty("")
    suggest = StringProperty("NoAction")
    owned = StringProperty("1BTC")
    price = NumericProperty(0.0)
    price_change = NumericProperty(0.0)
    slope = NumericProperty(0.0)
    chart_data = ListProperty([0, .1])
    daily_prices = ListProperty([0, .1])
    weekly_prices = ListProperty([0, .1])
    monthly_prices = ListProperty([0, .1])
    yearly_prices = ListProperty([0, .1])
    data = ObjectProperty()
    # Define the maximum number of requests allowed per minute
    MAX_REQUESTS_PER_MINUTE = 10
    # Store the timestamp_ of the last request
    last_request_time = None

    def __init__(self, **kv) -> None:
        super().__init__(**kv)
        self.coing = CoinGeckoAPI()
        self.from_view = False
        self.bind(on_release=self.view_asset)
    
    def on_price_change(self, inst, value):
        new_price = f"+{value}"
        new_price = new_price.replace("+-", "-")[:5]
        self.ids.price_change.text = new_price + "%"

        if new_price.startswith("-"):
            self.ids.price_change.color = App.get_running_app().colors.hazard

    def on_suggest(self, inst, value):
        new_price = f"{value}"
        new_price = new_price.replace("+-", "-")[:5]
        self.ids.suggest.text = new_price

        if new_price.startswith("-"):
            self.ids.suggest.color = App.get_running_app().colors.hazard

    def view_asset(self, *args):
        """
            Required
            ==========================
            cryptoCurrency = StringProperty("BTC")
            cryptoAsset_value = NumericProperty(42342.62)
            source = StringProperty("")
            chart_data = ListProperty([0,1])
            one_day_data = ListProperty([0,1])
            one_week_data = ListProperty([0,1])
            one_month_data = ListProperty([0,1])
            one_year_data = ListProperty([0,1])
        """
        if len(self.daily_prices) < 10:
            self.from_view = True
            self.get_data_()
        else:
            self.open_view()
    
    @mainthread
    def open_view(self):
        av = AssetView()
        av.cryptoCurrency = str(self.text)
        av.cryptoAsset_value = self.price
        av.source = self.source
        av.one_day_data = self.daily_prices
        av.one_week_data = self.weekly_prices
        av.one_month_data = self.monthly_prices
        av.one_year_data = self.yearly_prices
        av.data = self.data
        av.open()
        Clock.schedule_once(lambda x: av.update_graph(), .5)
    
    def get_data_(self):
        coin_id = self.data['id']

        t1_ = Thread(target=self.get_points, args=[coin_id], daemon=True)
        t1_.start()

    def get_points(self, coin_id):

        daily = self.make_api_request(coin_id, days=1)

        points = [x[1] for x in daily['prices'][-60:]]
        self.chart_data = points
        self.daily_prices = [x[1] for x in daily['prices']]

        t1_ = Thread(target=self.get_all_points, args=[coin_id], daemon=True)
        t1_.start()

    def get_all_points(self, coin_id):
        weekly = self.make_api_request(coin_id, days=7)
        monthly = self.make_api_request(coin_id, days=30)
        yearly = self.make_api_request(coin_id, days=365)

        self.weekly_prices = [x[1] for x in weekly['prices']]
        self.monthly_prices = [x[1] for x in monthly['prices']]
        self.yearly_prices = [x[1] for x in yearly['prices']]

        if self.from_view:
            self.open_view()
            self.from_view = False

    def make_api_request(self, coin_id, days):
        global last_request_time

        if 'last_request_time' not in locals():
            last_request_time = None  # or initialize with an appropriate value
        # Rest of your code

        # Check if the last request was made within the last minute
        if last_request_time is not None:
            elapsed_time = time.time() - last_request_time
            if elapsed_time < 60:
                # Sleep for the remaining time before making the next request
                time.sleep(60 - elapsed_time)

        # Make the API request
        if days is 1:
            response = self.coing.get_coin_market_chart_by_id(coin_id, vs_currency="usd", days=1)
        elif days is 7:
            response = self.coing.get_coin_market_chart_by_id(coin_id, vs_currency="usd", days=7)
        elif days is 30:
            response = self.coing.get_coin_market_chart_by_id(coin_id, vs_currency="usd", days=30)
        elif days is 365:
            response = self.coing.get_coin_market_chart_by_id(coin_id, vs_currency="usd", days=365)

        # Update the timestamp_ of the last request
        last_request_time = time.time()

        return response

class Asset(Card):
    def __init__(self, **kv) -> None:
        super().__init__(**kv)

        Clock.schedule_once(self.render_, .2)

    def render_(self, _):
        graph = self.ids.graph
        plot = LinePlot()
        plot.line_width = dp(1.2)
        plot.color = App.get_running_app().colors.thirdlevel_light

        graph.add_plot(plot)

    def on_data(self, *args):
        self.get_data_()
    
    def on_chart_data(self, inst, coinPrices):
        graph = self.ids.graph
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


class Asset2(Card):
    def __init__(self, **kv) -> None:
        super().__init__(**kv)

        Clock.schedule_once(self.render_, .2)

    def render_(self, _):
        graph = self.ids.graph

    def on_data(self, *args):
        self.get_data_()


class ListTile(Card):
    def __init__(self, **kv) -> None:
        super().__init__(**kv)
