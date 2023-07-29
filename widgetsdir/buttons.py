from kivy.uix.button import Button
from kivy.uix.button import StringProperty
from kivy.lang import Builder

from kivy.properties import ColorProperty
from kivy.properties import get_color_from_hex
from kivy.properties import ListProperty
from kivy.properties import colormap

from kivy.graphics import RoundedRectangle
from kivy.graphics import shader
from kivy.graphics import Color
from kivy.utils import rgba
from kivy.metrics import dp


Builder.load_string("""
<FlatButtonWidget>:
    text_size: self.size
    valign: "middle"
    halign: "center"
    markup: True

<IconButtonWidget>:
    canvas.after:
        Color:
            btn_color: root.btn_color
            rgba: root.bcolor
        Rectangle:
            pos: self.pos
            size: self.size
""")
class FlatButtonWidget(Button):
    def __init__(self, **kv):
        super().__init__(**kv)
        self.background_down = ""
        self.background_normal = ""
        self.background_color = [0.1,0,0,0]
        self.background_disabled = ""
        self.markup = True

class IconButtonWidget(FlatButtonWidget):
    bcolor = ColorProperty([0.1,0,0,0])
    def __init__(self, **kv):
        super().__init__(**kv)

class RoundedButton(FlatButtonWidget):
    bcolor = ColorProperty([1.1,1,1,0])
    radius = ListProperty([dp(2)])
    def __init__(self, **kv):
        super().__init__(**kv)

        with self.canvas.before:
            self.paintB = Color(rgba=self.bcolor)
            self.drawB = RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)

        self.bind(pos=self.update)
        self.bind(size=self.update)

    def update(self, *args):
        self.drawB.pos = self.pos
        self.drawB.size = self.size

    def on_radius(self, *args):
        self.drawB.radius = self.radius

    def on_bcolor(self, *args):
        self.paintB.rgba = self.bcolor