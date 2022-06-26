import tty
import termios
import sys
import os
import select
from game import Game
from numpy import copy as np_copy

arr = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]


class Interface:
    def __init__(self):
        self._x = 0
        self._y = 0
        self._game = Game()



    def start(self):
        cursor_x = 0
        cursor_y = 0
        orig_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin)
        self.print_cursor()
        try:
            while 1:
                if select.select([sys.stdin, ], [], [], 0.0)[0]:
                    inp = sys.stdin.read(1)
                    if inp == 'w':
                        self._x = max(0, self._x - 1)
                    if inp == 's':
                        self._x = min(9, self._x + 1)
                    if inp == 'a':
                        self._y = max(0, self._y - 1)
                    if inp == 'd':
                        self._y = min(9, self._y + 1)
                    if inp == 'q':
                        sys.exit(1)
                    if inp == 'f':
                        print(self._x, self._y)
                    self.print_cursor()
        except SystemExit as e:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
            sys.exit(e)

def print_cursor(cursor_x, cursor_y):

    game = Game()
    os.system('clear')
    game.print_board1((cursor_x, cursor_y))

def start(self):
    cursor_x = 0
    cursor_y = 0
    orig_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin)
    print_cursor(cursor_x,cursor_y)
    try:
        while 1:
            if select.select([sys.stdin, ], [], [], 0.0)[0]:
                inp = sys.stdin.read(1)
                if inp == 'w':
                    cursor_x = max(0, cursor_x - 1)
                if inp == 's':
                    cursor_x = min(9, cursor_x + 1)
                if inp == 'a':
                    cursor_y = max(0, cursor_y - 1)
                if inp == 'd':
                    cursor_y = min(9, cursor_y + 1)
                if inp == 'q':
                    sys.exit(1)
                if inp == 'f':
                    print(cursor_x, cursor_y)
                    return
                print_cursor(cursor_x, cursor_y)
    except SystemExit as e:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
        sys.exit(e)

start(Game())