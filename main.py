import kivy
import random
from AIbot import AIbot
from Symbol import Symbol
from ScreenMaker import MenuScreen, GameScreen, FinalScreen
kivy.require("1.10.1")

from kivy.app import App
from TicTacToe import TicTacToe
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock


class TicTacToeApp(App):

    game = ObjectProperty(None)
    sm = ObjectProperty(None)
    winning_screen = ObjectProperty(None)

    def build(self):

        menu = MenuScreen(name="Menu")
        self.winning_screen = FinalScreen(name="Win")
        self.sm = ScreenManager()
        self.game = GameScreen(False, name="Tic Tac Toe")
        self.sm.add_widget(menu)
        self.sm.add_widget(self.game)
        self.sm.add_widget(self.winning_screen)

        #Clock.schedule_interval(game.botTurn, 0.5)
        return self.sm

        #return Symbol()

    def new_game(self, human):
        if self.sm.has_screen("Tic Tac Toe"):
            self.sm.remove_widget(self.game)

        self.game = GameScreen(human, name="Tic Tac Toe")
        self.sm.add_widget(self.game)
        self.sm.current = "Tic Tac Toe"

    def display_winner(self, winner):
        self.winning_screen.update_winner(winner)
        self.sm.current = "Win"



if __name__ == "__main__":
    TicTacToeApp().run()