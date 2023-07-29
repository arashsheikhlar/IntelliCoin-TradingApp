from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock


Builder.load_file('viewsdir/home/homeview.kv')
class Home(BoxLayout):
    def __init__(self, **kv) -> None:
        super().__init__(**kv)
        Clock.schedule_once(self.render_, .2)

    def render_(self, _):
        pass
    