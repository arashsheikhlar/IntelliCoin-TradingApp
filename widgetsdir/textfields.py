
from kivy.uix.textinput import TextInput
from kivy.uix.textinput import Texture
from kivy.lang import Builder

Builder.load_string("""
<BlankTextFieldWidget>:
    foreground_color: app.colors.white
    background_normal: ""
    background_active: ""
    background_color: [0.1,0,0,0]
    padding: [dp(7), (self.height - self.line_height)/2]
""")

class BlankTextFieldWidget(TextInput):
    def __init__(self, **kv) -> None:
        super().__init__(**kv)