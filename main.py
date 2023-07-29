
from os.path import dirname
# from os.path import joinDir
from os.path import join

from kivy.garden.iconfonts import register

from app import Main

register("Feather", join(dirname(__file__), 'assets/fonts/feathers/feather.ttf'),
         join(dirname(__file__), 'assets/fonts/feathers/feather.fontd'),)
Main().run()
