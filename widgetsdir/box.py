
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.boxlayout import VariableListProperty
from kivy.properties import ColorProperty
from kivy.properties import ListProperty
from kivy.properties import BooleanProperty


Builder.load_string('''
<BackBoxWidget>:
    canvas.before:
        Color:
            rgba: self.bcolor
        RoundedRectangle:
            segments: 1        
            size: self.size
            pos: self.pos
            radius: self.radius

''')
class BackBoxWidget(BoxLayout):
    bcolor = ColorProperty([1.1,1,1,0])
    radius = ListProperty([.51])
    def __init__(self, **kv) -> None:
        super().__init__(**kv)
 
