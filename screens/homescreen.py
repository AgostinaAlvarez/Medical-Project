from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def switch_screen_search_user(self):
        self.manager.current = 'search_user_screen'

    def switch_screen_create_user(self):
        self.manager.current = 'create_user_screen'