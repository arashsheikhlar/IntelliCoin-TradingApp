
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from viewsdir.assetview import Alert
from kivy.lang import Builder
import os
import json
import hashlib


Builder.load_file('viewsdir/signin/signin.kv')
class Signin(BoxLayout):
    def __init__(self, **kv) -> None:
        super().__init__(**kv)
        self.alert = Alert()

    def signinF(self):
        uname = self.ids.username.text.strip()
        passw = self.ids.password.text.strip()

        self.ids.username.text = ""
        self.ids.password.text = ""

        if len(uname) < 4:
            self.alert.text = "Username is invalid"
            self.alert.open()
            return
        
        if len(passw) < 6:
            self.alert.text = "Password is invalid"
            self.alert.open()
            return

        passw = hashlib.sha256(bytes(passw, encoding="utf-8")).hexdigest()
        
        users = {}

        userPath = App.get_running_app().user_data_dir
        savePath = os.path.join(userPath, "users.json")
        if os.path.exists(savePath):
            with open(savePath, "r") as ft:
                users = json.load(ft)
        
        if uname in list(users.keys()):
            upass = users[uname]['password']

            if upass != passw:
                self.alert.text = "Password is incorrect"
                self.alert.open()
                return
            else:
                App.get_running_app().root.ids.screen_mngr.current = 'screen_home'
        else:
            self.alert.text = "User not found"
            self.alert.open()
            return
