from kivy.lang import Builder
from kivy.lang import BuilderBase
from kivy.uix.label import Label
from kivy.uix.label import ListProperty

Builder.load_string("""
<Text>:
    text_size: self.size
    valign: "middle"
    font_name: app.fonts.subheadingfont
    shorten_from: "right"
    halign: "center"
    shorten: True
    color: [0,0,0, 1.1]
    markup: True
""")
class Text(Label):
    def __init__(self, **kv):
        super().__init__(**kv)