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

    def collision(self, screen, player):
        # Obstacle is present below
        if screen.frame[self.x+1][self.y] != self.pixel(' '):
            if screen.frame[self.x+1][self.y] == self.pixel('▬'):
                self.paddle_collision(screen, player)
            else:
                self.motion['x'] = -self.motion['x']
        # Obstacle is present above
        if screen.frame[self.x-1][self.y] != self.pixel(' '):
            self.motion['x'] = -self.motion['x']
        # Obstacle is present to the right
        if screen.frame[self.x][self.y+1] != self.pixel(' '):
            self.motion['y'] = -self.motion['y']
        # Obstacle is present to the left
        if screen.frame[self.x][self.y-1] != self.pixel(' '):
            self.motion['y'] = -self.motion['y']

    def movement(self, screen, player):
        # Check collision
        self.collision(screen, player)
        # Copy position for reference
        self.prev['x'] = self.x
        self.prev['y'] = self.y
        # Update position
        self.x += self.motion['x']
        self.y += self.motion['y']
        # Render position
        self.render(screen)