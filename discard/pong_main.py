#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/2 16:17
# @Author  : Jago
# @Email   : 18146856052@163.com
# @File    : pong_main.py
# from random import randint

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity  # 获取乒乓速度
            offset = (ball.center_y - self.center_y) / (self.height / 2)  # 获取乒乓撞击球拍偏移
            bounced = Vector(-1 * vx, vy)  # x轴反向
            vel = bounced * 1.1  # 加速
            ball.velocity = vel.x, vel.y + offset  # 不管撞在上面还是下面，都会造成反向效果


class PongBall(Widget):
    # velocity of the ball on x and y axis
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    # referencelist property so we can use ball.velocity as
    # a shorthand, just like e.g. w.pos for w.x and w.y
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # ``move`` function will move the ball one step. This
    #  will be called in equal intervals to animate the ball
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self, vel=(4, 0)):  # 默认左边发球
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()
        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce off top and bottom
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        # bounce off left and right
        # if (self.ball.x < 0) or (self.ball.right > self.width):
        #     self.ball.velocity_x *= -1
        # went of to a side to score point?
        if self.ball.x < self.x:  # 右边赢球，左边发球
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > 2 * self.width / 3:
            self.player2.center_y = touch.y


class PongApp(App):
    def build(self):
        # return PongGame()
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)  # 60 times per second
        return game


if __name__ == '__main__':
    # The name of the kv file, e.g. pong.kv,
    # must match the name of the app,
    # e.g. PongApp (the part before the App ending).
    PongApp().run()
