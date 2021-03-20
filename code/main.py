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

Score = 0
Lives = 9
Time = time.time()
Level = 1

while True:
    screen = Render()
    player = Player(screen)
    ball = Ball(screen, player)
    bricks = Bricks(screen)
    bar = Bar(screen)
    
    bar.score = Score
    bar.lives = Lives
    bar.level = Level
    bar.start_time = Time

    while True:
        # Restart
        if player.movement(input_to(), screen):
            Score = 0
            Time = time.time()
            Lives = 10
            break
        # Endgame
        if bar.lives == 0:
            print('You just died. Lol haha xD')
            sys.exit()
        # Next Level
        lvlFlag = True
        for eachRow in range(bricks.begin['x'], bricks.end['x']):
            for eachCol in range(bricks.begin['y'], bricks.end['y']):
                if bricks.frame[eachRow][eachCol] in [1, 2, 3, 4]:
                    lvlFlag = False
                    break
            if lvlFlag == False:
                break
        if lvlFlag:
            Level += 1
            Score = bar.score
            Lives = bar.lives
            if Level != 9:
                break
            elif Level == 9:
                print('You just won. Holy Cow!!')
                sys.exit()
        # Render
        bar.render(screen)
        ball.movement(screen, player, bricks, bar)
        bricks.render(screen)
        ball.render(screen)
        screen.render(screen.margin, screen.frame)
        time.sleep(1/screen.fps)