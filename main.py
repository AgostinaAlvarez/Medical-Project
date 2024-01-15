from kivy.config import Config
# Obtener las dimensiones de la pantalla
#Config.set('graphics', 'width', '1600')
#Config.set('graphics', 'height', '850')

from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen,ScreenManager
from screens.homescreen import HomeScreen
from screens.searchuser import SearchUser
from screens.createuser import CreateUser
from screens.searchusercamera import SearchUserCamera
from screens.detailscreen import DetailScreen

class MainScreen (Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MainApp(MDApp):
    def build(self):
        return MainScreen()

MainApp().run()
