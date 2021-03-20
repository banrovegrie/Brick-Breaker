import copy, sys, time, os, math, subprocess as sp
import colorama as color, numpy as np
from colorama import Fore, Back, Style

debug_file = open("debug.log", "w")
debug_file.close()

class Ball:

    def pixel(self, ch, color=Fore.WHITE):
        return Back.BLACK + color + ch + Style.RESET_ALL

    def clear(self, screen):
        screen.frame[self.prev['x']][self.prev['y']] = self.pixel(' ')

    def render(self, screen):
        self.clear(screen)
        screen.frame[self.x][self.y] = self.pixel('●', Fore.GREEN)

    # Here x = row, and y = col
    def __init__(self, screen, player):
        self.prev = {
            'x': player.pos - 1,
            'y': int(screen.cols//2)
        }
        self.x = player.pos - 1
        self.y = int(screen.cols//2)
        self.motion = {
            'x': 1,                  # 0 is no motion, 1 is down, -1 is up
            'y': 1                   # 0 is no motion, 1 is right, -1 is left
        }
        self.render(screen)
    
    def paddle_collision(self, screen, player):
        dist = self.y - player.center
        self.motion['x'] = -1
        if abs(dist) > (2 * player.size)//3:
            self.motion['y'] = -2 if dist < 0 else 2
        elif abs(dist) > (player.size)//3:
            self.motion['y'] = -1 if dist < 0 else 1
        else: 
            self.motion['y'] = 0

    def golden_collision(self, bricks, i):
        for j in range(bricks.begin['y'], bricks.end['y']):
            if bricks.frame[i][j] == 4:
                bricks.frame[i+1][j] = 0
                bricks.frame[i-1][j] = 0
                bricks.frame[i][j-1] = 0
                bricks.frame[i][j] = 0


    def collision(self, screen, player, bricks, bar):
        # Obstacle is present below
        if screen.frame[self.x+1][self.y] != self.pixel(' ') and self.motion['x'] > 0:
            if screen.frame[self.x+1][self.y] == self.pixel('▬'):
                self.paddle_collision(screen, player)
            else:
                if bricks.frame[self.x+1][self.y] in [1, 2, 3]:
                    for j in range(int(bricks.center[self.x+1][self.y]-2), int(bricks.center[self.x+1][self.y]+3)):
                        bricks.rainbow[self.x+1][j] = 0
                        bricks.frame[self.x+1][j] -= 1
                        bar.score += 1
                elif bricks.frame[self.x+1][self.y] == 4:
                    self.golden_collision(bricks, self.x+1)
                    bar.score += 50
                elif screen.frame[self.x+1][self.y] == self.pixel('_'):
                    bar.lives -= 1
                self.motion['x'] = -self.motion['x']

        # Obstacle is present above
        if screen.frame[self.x-1][self.y] != self.pixel(' ') and self.motion['x'] < 0:
            if bricks.frame[self.x-1][self.y] in [1, 2, 3]:
                for j in range(int(bricks.center[self.x-1][self.y]-2), int(bricks.center[self.x-1][self.y]+3)):
                    bricks.rainbow[self.x-1][j] = 0
                    bricks.frame[self.x-1][j] -= 1
                    bar.score += 1
            elif bricks.frame[self.x-1][self.y] == 4:
                self.golden_collision(bricks, self.x-1)
                bar.score += 50
            self.motion['x'] = -self.motion['x']

        # Obstacle is present to the right
        if screen.frame[self.x][self.y+1] != self.pixel(' ') and self.motion['y'] > 0:
            if bricks.frame[self.x][self.y+1] in [1, 2, 3]:
                for j in range(int(bricks.center[self.x][self.y+1]-2), int(bricks.center[self.x][self.y+1]+3)):
                    bricks.rainbow[self.x][j] = 0
                    bricks.frame[self.x][j] -= 1
                    bar.score += 1
            elif bricks.frame[self.x][self.y+1] == 4:
                self.golden_collision(bricks, self.x)
                bar.score += 50
            self.motion['y'] = -self.motion['y']

        # Obstacle is present to the left
        if screen.frame[self.x][self.y-1] != self.pixel(' ') and self.motion['y'] < 0:
            if bricks.frame[self.x][self.y-1] in [1, 2, 3]:
                for j in range(int(bricks.center[self.x][self.y-1]-2), int(bricks.center[self.x][self.y-1]+3)):
                    bricks.rainbow[self.x][j] = 0
                    bricks.frame[self.x][j] -= 1
                    bar.score += 1
            elif bricks.frame[self.x][self.y-1] == 4:
                self.golden_collision(bricks, self.x)
                bar.score += 50
            self.motion['y'] = -self.motion['y']

    def movement(self, screen, player, bricks, bar):
        # Check collision
        self.collision(screen, player, bricks, bar)
        # Copy position for reference
        self.prev['x'] = self.x
        self.prev['y'] = self.y
        # Update position
        self.x += self.motion['x']
        self.y += self.motion['y']
        # Render position
        self.render(screen)