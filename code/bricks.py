import copy, sys, time, os, math, subprocess as sp
import colorama as color, numpy as np, random
from colorama import Fore, Back, Style

debug_file = open("debug.log", "w")
debug_file.close()

class Bricks:

    def pixel(self, ch, color=Fore.WHITE):
        return Back.BLACK + color + ch + Style.RESET_ALL

    def render(self, screen):
        for i in range(self.begin['x'], self.end['x']):
            for j in range(self.begin['y'], self.end['y']):
                if self.frame[i][j] == 1:
                    screen.frame[i][j] = self.pixel('█', Fore.MAGENTA)
                elif self.frame[i][j] == 2:
                    screen.frame[i][j] = self.pixel('█', Fore.CYAN)
                elif self.frame[i][j] == 3:
                    screen.frame[i][j] = self.pixel('█', Fore.BLUE)
                elif self.frame[i][j] == 4:
                    screen.frame[i][j] = self.pixel('█', Fore.YELLOW)
                elif self.frame[i][j] == 5: 
                    screen.frame[i][j] = self.pixel('█', Fore.WHITE)    

    def fill(self, screen):
        for i in range(self.begin['x'], self.end['x']):
            if i == self.golden[0]['x']:
                for j in range(self.begin['y']+10,self.begin['y']+60):
                    self.frame[i][j] = 4
            elif i == self.golden[1]['x']:
                for j in range(self.begin['y']+10,self.begin['y']+60):
                    self.frame[i][j] = 4
            else:
                for j in range(self.begin['y'], self.end['y'], 5):
                    if random.choice(self.prob):
                        option = random.choice(self.options)
                        for k in range(j, j+5):
                            self.frame[i][k] = option

    def __init__(self, screen):
        self.frame = np.zeros((screen.rows, screen.cols))
        self.prob = [0, 0, 0, 1]
        self.options = [1, 1, 2, 2, 3, 3, 5]         # 0 = no brick, 4 = golden, 5 = unbreakable
        self.begin = {
            'x': int(screen.rows * 0.2),
            'y': int(screen.cols * 0.15)
        }
        self.end = {
            'x': int(screen.rows * 0.55),
            'y': int(screen.cols * 0.85)
        }
        self.golden = [{
            'x': random.choice([i for i in range(self.begin['x'], self.end['x'])])
        },
        {
            'x': random.choice([i for i in range(self.begin['x'], self.end['x'])])
        }]

        self.fill(screen)
        self.render(screen)