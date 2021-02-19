import copy, sys, time, os, math, subprocess as sp
import colorama as color, numpy as np
from colorama import Fore, Back, Style

debug_file = open("debug.log", "w")
debug_file.close()

class Player:

    def pixel(self, ch):
        return Back.BLACK + Fore.WHITE + ch + Style.RESET_ALL

    def clear(self, screen):
        screen.frame[self.pos:self.pos+1, 1:screen.cols-1] = self.pixel(' ')

    def render(self, screen):
        self.clear(screen)
        screen.frame[self.pos:self.pos+1, 
            self.center-self.size:self.center+self.size] = self.pixel('▬')

    def check_if_at_end(self, screen):
        self.at_left = (self.center-self.size <= 0)
        self.at_right = (self.center+self.size >= screen.cols - 1)
        
        if self.at_left:
            self.center = self.size + 1
        elif self.at_right:
            self.center = screen.cols - self.size - 1        

    def __init__(self, screen):
        self.pos = int(0.85 * screen.rows)
        self.size = int(4 + 0.03 * (screen.cols))
        self.center = int(screen.cols//2)
        
        self.at_left = False
        self.at_right = False

        self.check_if_at_end(screen)
        self.render(screen)

    def movement(self, Inp, screen):
        if Inp == 'q':
            sys.exit()
        elif Inp == 'a' or Inp == 'A':
            self.center -= 1
            self.check_if_at_end(screen)
            self.render(screen)
        elif Inp == 'd' or Inp == 'D':
            self.center += 1
            self.check_if_at_end(screen)
            self.render(screen)
        elif Inp == 'r' or Inp == 'R':
            return True
        return False