import random
from kivy.properties import ListProperty


class AIbot:

    mark = "O"
    opponent = "X"
    level = 0
    turn = -1
    ai_choice = -1
    indent = ""

    def __init__(self, mark):
        self.mark = mark
        print("TESTTTT")
        if self.mark == "X":
            self.opponent = "O"


    def draw_tree(self, board):
        drawing = []
        for item in board:
            if item == -1:
                drawing.append(self.bot)
            elif item == 1:
                drawing.append(self.opponent)
            else:
                drawing.append("-")

        print(self.indent, end="")
        for index, value in enumerate(drawing):
            print(value, "|", end=""),

            if index == 2 or index == 5:
                print(""),
                print(self.indent, end="")
        print("")


    def print_moves(self, board):
        print("Printing AI moves... ", self.get_free_moves(board))

    def get_free_moves(self, board):
        return [index for index, value in enumerate(board) if value == 0]

    def check_winner(self, main_board, level):
        status = main_board
        sums = [sum(status[0:3]), sum(status[3:6]), sum(status[6:9]), sum(status[0::3]),sum(status[1::3]),
                sum(status[2::3]),sum(status[::4]), sum(status[2:-2:2])]

        if 3 in sums:
            return level - 10
        elif -3 in sums:
            return 10 - level
        else:
            return 0

    def play_dumb(self, board):
        print("Playing dumb...")
        self.draw_tree(board)
        free = self.get_free_moves(board)
        dumb_move = random.choice(free)
        return dumb_move

    def play(self, board):
        print("Playing...")

        def get_new_state(move, board, turn):
            board[move] = turn
            return board

        def minmax(status, level, turn):
            board = list(status)
            free = self.get_free_moves(board)
            if len(free) == 0:
                print(self.indent, "REACHED THE END, RETURNING ", self.check_winner(board, level))
                self.draw_tree(board)
                return self.check_winner(board, level)
            else:
                scorelist = []
                moves = []
                level += 1
                self.indent = self.indent + "-"

                # Populate Arrays
                for move in free:
                    print(self.indent, "PROCESSING MOVE ", move)
                    new_state = get_new_state(move, list(board), turn)

                    current_winner = self.check_winner(new_state, level)
                    if current_winner == 0 :
                        scorelist.append(minmax(new_state, level, turn*-1))
                    else:
                        print(self.indent, "NO NEED TO ENTER MINMAX...RETURNING ", current_winner)
                        self.draw_tree(new_state)
                        scorelist.append(current_winner)
                    moves.append(move)

                print(self.indent, "CURRENT SCORE LIST: ", scorelist)
                if turn == -1:
                    max_score_index = scorelist.index(max(scorelist))
                    self.ai_choice = moves[max_score_index]
                    self.draw_tree(board)
                    print(self.indent, "IN MAXIMUM - DEPTH: ", level, "BEST MOVE: ", self.ai_choice, " RETURNING SCORE: ", scorelist[max_score_index])
                    print(self.indent, "END MOVE ", move)
                    print(self.indent, "---------------")
                    self.indent = self.indent[:-1]
                    return scorelist[max_score_index]
                else:
                    print(self.indent, "CURRENT SCORE LIST: ", scorelist)
                    min_score_index = scorelist.index(min(scorelist))
                    self.ai_choice = moves[min_score_index]
                    self.draw_tree(board)
                    print(self.indent, "IN MINIMUM - DEPTH: ", level, "OPPONENT BEST MOVE: ", self.ai_choice, " RETURNING SCORE: ", scorelist[min_score_index])
                    print(self.indent, "END MOVE ", move)
                    print(self.indent, "---------------")
                    self.indent = self.indent[:-1]
                    return scorelist[min_score_index]


        minmax(board, self.level,-1)
        return self.ai_choice