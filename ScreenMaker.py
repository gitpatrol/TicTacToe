from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, StringProperty
from TicTacToe import TicTacToe

class MenuScreen(Screen):
    pass

class FinalScreen(Screen):

    def __init__(self, **kwargs):
        super(FinalScreen, self).__init__(**kwargs)

    def update_winner(self, winner):
        self.ids.floatcont.add_widget(Label(text=winner))


class GameScreen(Screen):

    def __init__(self, human, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.add_widget(TicTacToe(human))