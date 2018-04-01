import kivy
from Player import Player, AIbot
kivy.require("1.10.1")

from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics import Line
from kivy.animation import Animation
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, BooleanProperty, StringProperty
from kivy.event import*

Window.size=(480,853)


class GridEntry(RelativeLayout):

    coords = ListProperty([0, 0])
    btnID = ObjectProperty()
    img = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(GridEntry, self).__init__(**kwargs)


class PlayerChooser(Popup):

    game = ObjectProperty()

    def close(self, button):
        if button == "X":
            self.game.player1 = Player(True, 1, "Player 1")
            self.game.player2 = AIbot(-1)
            self.game.currentPlayer = self.game.player1
        elif button == "O":
            self.game.player1 = AIbot(1)
            self.game.player2 = Player(True, -1, "Player 2")
            self.game.currentPlayer = self.game.player1
            self.game.bot_play(0)

        self.dismiss()


class TicTacToe(BoxLayout, EventDispatcher):

    status = ListProperty([0, 0, 0, 0, 0, 0, 0, 0, 0])
    grid_size = (NumericProperty(0), NumericProperty(0))

    start = False
    level = 0
    game_over = False
    human = False
    button_size = None
    duration = 0.35
    ai_level = 1

    def __init__(self, human, *args, **kwargs):

        super(TicTacToe, self).__init__(*args, **kwargs)
        self.human = human
        count = 0

        for row in range(3):
            for col in range(3):
                count += 1
                grid_entry = GridEntry(
                    coords=(row, col))
                grid_entry.btnID = count
                #grid_entry.add_widget(Label(text=str(count), id="btntext"))
                grid_entry.ids.container.bind(on_release=self.button_pressed)
                self.ids.playboard.add_widget(grid_entry)

        if self.human:
            self.player1 = Player(True, 1, "Player 1")
            self.currentPlayer = self.player1
            self.player2 = Player(False, -1, "Player 2")
        else:
            popup = PlayerChooser(game=self)
            popup.open()



    def is_game_over(self, board):

        free = self.player2.get_free_moves(board)
        if len(free) == 0:
            return True
        else:
            return False

    def check_game(self,dt):
        print("CURRENT BOARD: ", self.status, " Current Player: ", self.currentPlayer.name)

        if self.is_game_over(self.status):
            self.game_over = True

        winner = self.currentPlayer.check_winner(self.status, 0)

        if winner == 10:
            print("GAME OVER! PLAYER 2 WINS!")
            self.game_over = True
            self.ids.champ.text = self.player2.name + " WINS"
            print(self.currentPlayer.get_winning_coords(self.status))
            self.draw_winner(self.currentPlayer.get_winning_coords(self.status))

        elif winner == -10:
            print("GAME OVER! PLAYER 1 WINS!")
            self.game_over = True
            self.ids.champ.text = self.player1.name + " WINS"
            print(self.currentPlayer.get_winning_coords(self.status))
            self.draw_winner(self.currentPlayer.get_winning_coords(self.status))

        elif self.game_over:
            print("GAME OVER! DRAW!")
            self.ids.champ.text = "DRAW"
            print(self.currentPlayer.get_winning_coords(self.status))

        else:
            print("CONTINUE PLAYING")

    def button_pressed(self, button):

        print("BUTTON IS PRESSED ", button.size)
        print("CURRENT PLAYER", self.currentPlayer.name)


        if not self.game_over:
            self.start = True

            row, col = button.parent.coords
            status_index = self.convertCoords(row, col)

            button.draw(self.currentPlayer.symbol)
            button.disabled = True


            if self.human:
                self.status[status_index] = self.currentPlayer.id

                if self.currentPlayer == self.player1:
                    self.currentPlayer = self.player2
                else:
                    self.currentPlayer = self.player1

                self.check_game(None)
            else:

                self.status[status_index] = self.currentPlayer.id

                if self.currentPlayer == self.player1:
                    self.currentPlayer = self.player2
                else:
                    self.currentPlayer = self.player1

                self.check_game(None)
                if not self.game_over:
                    #Delay AI for 1 second and checks if AI wins
                    Clock.schedule_once(self.bot_play, 1)
                    Clock.schedule_once(self.check_game, 1)


    def bot_play(self, dt):

        robot = self.currentPlayer

        robot.print_moves(self.status)

        if self.level >= self.ai_level:
            ai_move = robot.play(list(self.status))
            print("LEVEL: ", self.level, "AI MOVE: ", ai_move)

        else:
            ai_move = robot.play_dumb(list(self.status))

        if not self.is_game_over(self.status):
            self.status[ai_move] = robot.id
            ai_btn = self.get_button(ai_move + 1)
            ai_btn.draw(robot.symbol)
            ai_btn.disabled = True

            self.level += 1
        else:
            self.game_over = True

        #Set next player to current
        if self.currentPlayer == self.player1:
            self.currentPlayer = self.player2
        else:
            self.currentPlayer = self.player1

    def update(self, button):
        row, col = button.parent.coords
        status_index = self.convertCoords(row, col)

        button.draw(self.currentPlayer.symbol)
        button.disabled = True

        if self.human:
            if self.currentPlayer == self.player1:
                self.currentPlayer = self.player2
                self.status[status_index] = 1
            else:
                print("PLAYER 2")
                self.status[status_index] = -1
                self.currentPlayer = self.player1
        else:
            self.status[status_index] = 1
            self.bot_play()

    def draw_winner(self, coords):

        def fade_board(win_ids):
            for box in self.ids.playboard.children:
                if box.btnID not in win_ids:
                    Animation(opacity=0.70, d=self.duration).start(box.ids.overlay)
                    Animation(opacity=0.20, d=self.duration).start(self.ids.bg)

        origin = 20
        width = self.ids.lineboard.width - origin
        height = self.ids.lineboard.height - origin

        padding = 10
        self.button_size = self.ids.playboard.children[0].ids.container.size
        grid_width = self.button_size[0] - padding
        grid_height = self.button_size[1]
        print("Winning coords: ", coords, "Pos: ", self.ids.playboard.size)
        index = coords[0]
        line = None

        if index == 0:
            y = (height - (grid_height/2)) + (origin - padding/2)
            line = Line(points=(origin, y, width, y), width=5)

            fade_board([1,2,3])

        elif index == 1:
            y = (height / 2) + (origin - padding)
            line = Line(points=(origin, y, width, y), width=5)

            fade_board([4, 5, 6])
        elif index == 2:
            y = (grid_height / 2) + padding/2
            line = Line(points=(origin, y, width, y), width=5)

            fade_board([7, 8, 9])
        elif index == 3:
            x1= (grid_width/2) + padding
            y1 = height
            x2 = x1
            y2 = origin
            line = Line(points=(x1,y1,x2,y2), width=5)

            fade_board([1, 4, 7])
        elif index == 4:
            x1= (width/2)+ padding
            y1 = height
            x2 = x1
            y2 = origin
            line = Line(points=(x1,y1,x2,y2), width=5)

            fade_board([2, 5, 8])
        elif index == 5:
            x1= (width - grid_width/2) + padding
            y1 = height
            x2 = x1
            y2 = origin
            line = Line(points=(x1,y1,x2,y2), width=5)

            fade_board([3, 6, 9])
        elif index == 6:
            line = Line(points=(origin, height, width, origin), width=5)

            fade_board([1, 5, 9])
        elif index == 7:
            line = Line(points=(width, height, origin, origin), width=5)

            fade_board([3, 5, 7])


    def convertCoords(self, row, col):
        return 3*row + col

    def get_button(self, btnID):

        for child in self.ids.playboard.children:

            if child.btnID == btnID:
                return child.ids.container
