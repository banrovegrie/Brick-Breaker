import copy, sys, time, os, math, subprocess as sp
import colorama as color, numpy as np, random
from colorama import Fore, Back, Style

debug_file = open("debug.log", "w")
debug_file.close()

class Top:

    def __init__(self, screen):
        self.begin = {
            1: 1, 
            2: screen.cols//2,
            3: screen.cols - 15 
        }
        self.row = 1

class Bar(Top):

    def pixel(self, ch, color=Fore.WHITE):
        return Back.BLACK + color + ch + Style.RESET_ALL

    def render(self, screen):
        screen.frame[self.row][self.begin[1]] = self.pixel('S')
        screen.frame[self.row][self.begin[1]+1] = self.pixel('c')
        screen.frame[self.row][self.begin[1]+2] = self.pixel('o')
        screen.frame[self.row][self.begin[1]+3] = self.pixel('r')
        screen.frame[self.row][self.begin[1]+4] = self.pixel('e')
        screen.frame[self.row][self.begin[1]+5] = self.pixel(':')
        screen.frame[self.row][self.begin[1]+7] = self.pixel(str(self.score//100))
        screen.frame[self.row][self.begin[1]+8] = self.pixel(str((self.score%100)//10))
        screen.frame[self.row][self.begin[1]+9] = self.pixel(str(self.score%10))

        screen.frame[self.row][self.begin[2]] = self.pixel('♥', Fore.RED)
        screen.frame[self.row][self.begin[2]+2] = self.pixel('✗')
        screen.frame[self.row][self.begin[2]+4] = Back.BLACK + str(self.lives) + Style.RESET_ALL

        self.time = int(time.time() - self.start_time)
        screen.frame[self.row][self.begin[3]] = self.pixel('T')
        screen.frame[self.row][self.begin[3]+1] = self.pixel('i')
        screen.frame[self.row][self.begin[3]+2] = self.pixel('m')
        screen.frame[self.row][self.begin[3]+3] = self.pixel('e')
        screen.frame[self.row][self.begin[3]+4] = self.pixel(':')
        screen.frame[self.row][self.begin[3]+6] = self.pixel(str(self.time//100))
        screen.frame[self.row][self.begin[3]+7] = self.pixel(str((self.time%100)//10))
        screen.frame[self.row][self.begin[3]+8] = self.pixel(str(self.time%10))

    def __init__(self, screen):
        super().__init__(screen)
        self.score = 0
        self.lives = 9
        self.start_time = time.time()
        self.render(screen)