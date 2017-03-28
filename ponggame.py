from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label

Builder.load_file("pong.kv")

# Class tennis paddle
class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 4)
            bounced = Vector(-1 * vx, vy)
            if abs(ball.velocity_x) < self.width:
                vel = bounced * 1.1
            else:
                vel=bounced
            ball.velocity = vel.x, vel.y + offset

# Class tennis ball
class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)


    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    global win_label

    def winner_check(self):
        winner = ''
        maxScore = 10
        if self.player1.score == maxScore:
            Clock.unschedule(gs.game.update)
            gs.game.boxwinner.opacity = 1
            gs.game.gamewinner.text = 'Winner: Player 1!'

        elif self.player2.score == maxScore:
            Clock.unschedule(gs.game.update)
            gs.game.boxwinner.opacity = 1
            gs.game.gamewinner.text = 'Winner: Player 2!'


    def update(self, dt):
        self.ball.move()

        self.winner_check()


        # bounced paddle
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounced top and bottom edge screen
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

            # going beyond the field and calculating player points
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        # left paddle
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y

        # right paddle
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y

        # swipe center menu for pause
        if self.width / 3 < touch.x < self.width - self.width / 3:
            sm.current = "pauseScreen"
            Clock.unschedule(gs.game.update)

# Declare both screens
class MenuScreen(Screen):
    def start_game(self):

        gs.game.player1.score = 0
        gs.game.player2.score = 0
        gs.game.gamewinner.text = ''
        gs.game.boxwinner.opacity = 0
        sm.current="gameScreen"
        gs.game.serve_ball()
        Clock.unschedule(gs.game.update)
        Clock.schedule_interval(gs.game.update, 1.0 / 60.0)

class GameScreen(Screen):
    game = ObjectProperty(None)

class PauseScreen(Screen):

    def start_game(self):

        gs.game.player1.score = 0
        gs.game.player2.score = 0
        gs.game.gamewinner.text = ''
        gs.game.boxwinner.opacity = 0
        sm.current="gameScreen"
        gs.game.serve_ball()
        Clock.unschedule(gs.game.update)
        Clock.schedule_interval(gs.game.update, 1.0 / 60.0)

    def resume_game(self):
        sm.current = 'gameScreen'
        Clock.schedule_interval(gs.game.update, 1.0 / 60.0)


# Create the screen manager
sm = ScreenManager()
gs = GameScreen(name='gameScreen')
sm.add_widget(MenuScreen(name='menuScreen'))
sm.add_widget(PauseScreen(name='pauseScreen'))
sm.add_widget(gs)


class PongApp(App):

    def build(self):
        self.title = 'TENNIS retro'
        return sm

if __name__ == '__main__':
    PongApp().run()
