from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class SearchUser(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def switch_screen_camera(self):
        self.manager.current = 'search_user_camera'