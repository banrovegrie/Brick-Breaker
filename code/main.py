import copy, sys, time, os, math, subprocess as sp
from input import input_to
from types import FrameType
import colorama as color, numpy as np
from colorama import Fore, Back, Style

debug_file = open("debug.log", "w")
debug_file.close()

color.init()

from render import Render
from player import Player
from ball import Ball
from bricks import Bricks
from bar import Bar

while True:
    screen = Render()
    player = Player(screen)
    ball = Ball(screen, player)
    bricks = Bricks(screen)
    bar = Bar(screen)

    while True:
        if player.movement(input_to(), screen):
            break
        if bar.lives == 0:
            print('You just died. Lol haha xD')
            sys.exit()
        bar.render(screen)
        ball.movement(screen, player, bricks, bar)
        bricks.render(screen)
        ball.render(screen)
        screen.render(screen.margin, screen.frame)
        time.sleep(1/screen.fps)