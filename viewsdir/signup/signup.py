
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from viewsdir.assetview import Alert
from kivy.lang import Builder
import os
import json
import hashlib



from viewsdir.assetview import Alert

Builder.load_file('viewsdir/signup/signup.kv')
class Signup(BoxLayout):
    def __init__(self, **kv) -> None:
        super().__init__(**kv)
        self.alert = Alert()

    def signup(self):
        uname = self.ids.username.text.strip()
        passw = self.ids.password.text.strip()

        self.ids.username.text = ""
        self.ids.password.text = ""

        if len(uname) < 4:
            self.alert.text = "The username must be longer than 3 characters"
            self.alert.open()
            return
        
        if len(passw) < 6:
            self.alert.text = "The password must be longer than 5 characters"
            self.alert.open()
            return
        
        users = {}
        userPath = App.get_running_app().user_data_dir
        savePath = os.path.join(userPath, "users.json")
        if os.path.exists(savePath):
            with open(savePath, "r") as ft:
                users = json.load(ft)
        
        user = {
                "username": uname,
                "password": hashlib.sha256(bytes(passw, encoding="utf-8")).hexdigest(),
            }

        users[uname] = user

        with open(savePath, "w") as ft:
            json.dump(users, ft)
        
        App.get_running_app().root.ids.screen_mngr.current = 'screen_signin'
        
