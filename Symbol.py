from kivy.uix.widget import Widget
from kivy.graphics import Line,InstructionGroup, Color, Ellipse, Bezier, Rectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.app import App


class Symbol(ButtonBehavior, Widget):

    d = 0.25
    t = "in_quad"
    origin = 20
    stroke_size = 5

    def draw(self, player):

        if player == "X":
            self.draw_x()
        elif player == "O":
            self.draw_o()

    def draw_x(self):

        print(self.size[0], "----", self.size[1])
        origin = self.origin
        width = self.size[0] - origin
        height = self.size[1] - origin

        def draw_right(widget, item):
            self.rl = Line(points=[width, height, width, height], width=self.stroke_size, joint="round", close="False",
                           cap="round")
            self.canvas.add(self.rl)
            right = Animation(points=[origin, origin, width, height], d=self.d)
            right.start(self.rl)

        ll = Line(points=[origin, height, origin, height], width=self.stroke_size, joint="round", close="False", cap="round")
        self.canvas.add(ll)
        print("X PARENT:", self.parent.btnID)
        left = Animation(points=[origin, height, width, origin], d=self.d, t=self.t)
        left.bind(on_complete=draw_right)
        left.start(ll)

    def draw_o(self):

        origin = self.origin
        stroke_size = 18
        width = self.size[0] - origin
        height = self.size[1] - origin

        pos_temp = [self.center_x - width / 2, self.center_y - height / 2]
        circ = Ellipse(size=[width,height],pos=pos_temp, angle_start=0, angle_end=1)

        width2 = width-stroke_size
        height2 = height-stroke_size
        pos_temp2 = [self.center_x - width2 / 2, self.center_y - height2 / 2]

        inner = InstructionGroup()
        inner.add(Color(0,210/255,210/255))
        inner.add(Ellipse(size=[width2,height2],pos=pos_temp2 ))
        self.canvas.add(circ)
        self.canvas.add(inner)
        circ_anim = Animation(angle_end=360, d=self.d, t=self.t)
        circ_anim.start(circ)






