import copy, sys, time, os, math, subprocess as sp
import colorama as color, numpy as np
from colorama import Fore, Back, Style

debug_file = open("debug.log", "w")
debug_file.close()

class Render:

    # Check terminal size 
    def check(self):
        if self.Rows <= 20 or self.Cols <= 75:
            print(f"You require a bigger terminal size in order to play this game.")
            sys.exit()
    
    def pixel(self, ch):
        return Back.BLACK + Fore.WHITE + ch + Style.RESET_ALL
    
    def mountBackground(self):
        self.frame[:] = self.pixel(' ')

    def mountBoard(self):
        self.frame[2][0] = self.pixel('.')
        self.frame[2][self.cols-1] = self.pixel('.')
        self.frame[2:3, 1:self.cols-1] = self.pixel('_')
        self.frame[self.rows-2:self.rows-1] = self.pixel('_')
        self.frame[3:self.rows-1, 0:1] = self.pixel('|')
        self.frame[3:self.rows-1, self.cols-1:] = self.pixel('|')

    # Define the class
    def __init__(self):
        self.fps = 25
        self.ratio = 0.9
        self.Rows = int(sp.getoutput("tput lines"))
        self.Cols = int(sp.getoutput("tput cols"))

        self.rows = int(self.Rows * self.ratio)
        self.cols = int(self.Cols * self.ratio)
        self.margin = {
            'rows': (self.Rows - self.rows)//2, 
            'cols': (self.Cols - self.cols)//2
        }
        self.frame = np.zeros((self.rows, self.cols), dtype="<U20")
        
        os.system('clear')
        self.mountBackground()
        self.check()
        self.mountBoard()

    # Render frame
    @staticmethod
    def render(margin, frame):
        print(f"\033[H\033[J\033[{int(margin['rows'])};1H", end="")
        # np.savetxt(sys.stdout, frame, fmt='%s', delimiter='', newline='\n')
        out = [" " * margin['cols'] + "".join(str) for str in frame]       # array of strings
        out = "\n".join(out)                                               # string
        print(out, flush=True)