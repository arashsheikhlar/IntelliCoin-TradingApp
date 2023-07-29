import os, json
from .view import MainWindow
from api import Kraken
from api import OKcoin
from kivy.app import App
from kivy.utils import rgba
from kivy.utils import QueryDict
from kivy.metrics import dp



class Main(App):
    colors = QueryDict()
    colors.backg = rgba("#0A051A")
    colors.successful = rgba("#15C097")
    colors.alarm = rgba("#F2C94C")
    colors.hazard = rgba("#EB5757")
    colors.thirdlevel = rgba("#19122F")
    colors.thirdlevel_light = rgba("#464058")
    colors.grey_dark = rgba("#c4c4c4")
    colors.grey_dark2 = rgba("#5a5a5a")
    colors.grey_light = rgba("#f5f5f5")
    colors.black = rgba("#a1a1a1")
    colors.white = rgba("#ffffff")
    colors.dark_green = rgba("#006400")
    colors.Royal_Blue = rgba('#4169E1')
    colors.Emerald_Green = rgba('#50C878')
    colors.Crimson_Red = rgba('#DC143C')
    colors.Golden_Yellow = rgba('#FFD700')
    colors.Orchid_Purple = rgba('#DA70D6')
    colors.Teal_Blue = rgba('#008080')
    colors.Coral_Pink = rgba('#FF7F50')
    colors.Lavender_Purple = rgba('#E6E6FA')
    colors.Sunflower_Yellow = rgba('#FFC512')
    colors.Sky_Blue = rgba('#87CEEB')
    colors.Ruby_Red = rgba('#E0115F')
    colors.Lime_Green = rgba('#00FF00')
    colors.Indigo_Blue = rgba('#4B0082')
    colors.Peach_Orange = rgba('#FFDAB9')
    colors.Mauve_Pink = rgba('#E0B0FF')
    colors.original = colors.grey_dark2
    colors.subordinate = [1, 1, 1, .2]


    fonts = QueryDict()
    fonts.size = QueryDict()
    fonts.size.s0 = dp(30)
    fonts.size.s1 = dp(24)
    fonts.size.s2 = dp(22)
    fonts.size.s3 = dp(18)
    fonts.size.s4 = dp(16)
    fonts.size.s5 = dp(14)
    fonts.size.s6 = dp(12)
    fonts.size.s7 = dp(11)
    fonts.size.s8 = dp(10)
    fonts.size.s9 = dp(9)
    fonts.size.s10 = dp(8)
    fonts.size.extralarge = dp(32)

    fonts.headingfont = 'assets/fonts/Inter/Inter-Bold.otf'
    fonts.subheadingfont = 'assets/fonts/Inter/Inter-Regular.otf'
    fonts.bodyfont = 'assets/fonts/Inter/Inter-Light.otf'

    okcoin = OKcoin()
    kraken = Kraken()



    def build(self):
        userPath = self.user_data_dir
        savePath = os.path.join(userPath, "keys.json")
        if os.path.exists(savePath):
            with open(savePath, "r") as ft:
                allkeys = json.load(ft)
            
            k = [x for x in allkeys.keys()]

            if 'KRAKEN' in k:
                self.kraken.api_key = allkeys['KRAKEN']['keys']['key']
                self.kraken.api_sec = allkeys['KRAKEN']['keys']['secret']

            if 'OKCOIN' in k:
                self.okcoin.api_key = allkeys['OKCOIN']['keys']['key']
                self.okcoin.api_sec = allkeys['OKCOIN']['keys']['secret']
                self.okcoin.pass_phrase = allkeys['OKCOIN']['keys']['passphrase']

        return MainWindow()
