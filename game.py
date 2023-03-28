import errors
from constant import SHIPS_COUNT, ALPHABET, INDENT_WIDTH, DIRR, WIN_MSG
from constant import LEN, LEGEND, LOSE_MSG, POINT_INPUT_TEXT
from constant import UNALLOWED_SHOT_TARDET, ROTATION_ERROR_TEXT
from constant import POINT_SHIP_INPUT_TEXT, SHIP_UNALLOWED_POSITION

from board import Board
from ship import Ship
from numpy.random import choice as np_choice
from random import choice
from os import system, name
from sys import stdin, exit


if name == 'nt':
    import msvcrt
else:
    import tty
    import termios


class Game():
    def __init__(self):
        self._board_bot = Board()
        self._board_player = Board()
        self._cursor_x = 0
        self._cursor_y = 0
        self._dirr = DIRR[0]
        self._area = set()
        if INDENT_WIDTH < 1:
            raise errors.InvalidIndentValue()

    def get_area(self, ship_size):
        area = set()
        if self._dirr == DIRR[0]:
            for i in range(ship_size):
                if self._cursor_y + i not in range(LEN):
                    raise errors.RotateError()
                area.add((self._cursor_x, self._cursor_y + i))
        else:
            for i in range(ship_size):
                if self._cursor_x + i not in range(LEN):
                    raise errors.RotateError()
                area.add((self._cursor_x + i, self._cursor_y))
        self._area = area

    def add_indent(self, line1, line2=None):
        indent = f"{' '*INDENT_WIDTH}|{' '*INDENT_WIDTH}"
        if line2:
            return line1 + indent + line2
        return line1 + indent + line1

    def add_whitespace(self, line):
        return f'{line} '

    def toggle_dirr(self):
        i = 1 + DIRR.index(self._dirr)
        self._dirr = DIRR[i % 2]

    def shot_player(self):
        self.print_board([], [(self._cursor_x, self._cursor_y)], bot=False,
                         msg=POINT_INPUT_TEXT)
        while 1:
            point = self.get_input_shot()
            flag = self._board_bot.shot(point)
            if flag is None:
                print(UNALLOWED_SHOT_TARDET, end='\r')
            elif flag is True:
                self.print_board([], [(self._cursor_x, self._cursor_y)],
                                 bot=False, msg=POINT_INPUT_TEXT)
            elif flag is False:
                break

    def shot_bot(self):
        while 1:
            point = self.get_point_for_shot()
            if self._board_player.shot(point) is False:
                break

    def get_point_for_shot(self):
        if self._board_player.get_damaged_ship():
            damaged_ship, damaged_units = self._board_player.get_damaged_ship()
            if len(damaged_units) > 1:
                if DIRR[0] == damaged_ship.get_dirr():
                    point_x = next(iter(damaged_units))[0]
                    y_list = [square[1] for square in damaged_units]
                    point_y = choice((max(y_list) + 1, min(y_list) - 1))
                else:
                    point_y = next(iter(damaged_units))[1]
                    x_list = [square[0] for square in damaged_units]
                    point_x = choice((max(x_list) + 1, min(x_list) - 1))
                point = (point_x, point_y)
            else:
                point_x = next(iter(damaged_units))[0]
                point_y = next(iter(damaged_units))[1]
                point = choice([(point_x, point_y + 1), (point_x, point_y - 1),
                                (point_x + 1, point_y), (point_x - 1, point_y)
                                ])
        else:
            point = tuple(np_choice(LEN, 2))
        return point

    def get_random_point(self):
        return tuple(np_choice(LEN, 2))

    def set_random_ships(self):
        for ship_size in SHIPS_COUNT:
            for _ in range(SHIPS_COUNT[ship_size]):
                while 1:
                    point = self.get_random_point()
                    dirr = choice(DIRR)
                    if self._board_bot.set_ship(Ship(point, int(ship_size),
                                                     dirr)):
                        break

    def set_ships(self):
        self.print_board()
        try:
            for ship_size in SHIPS_COUNT:
                for _ in range(SHIPS_COUNT[ship_size]):
                    ship_size = int(ship_size)
                    self.get_area(ship_size)
                    msg = POINT_SHIP_INPUT_TEXT.format(ship_size=ship_size)
                    self.print_board(self._area, [], bot=True, msg=msg)
                    while 1:
                        ship = self.get_input_ship(ship_size)
                        if self._board_player.set_ship(ship):
                            self.print_board(self._area, [], bot=True, msg=msg)
                            break
                        print(SHIP_UNALLOWED_POSITION, end='\r')
        except errors.RandomSet:
            self.print_board()

    def get_input(self):
        if name == 'nt':
            inp = str(msvcrt.getch())[2]
        else:
            inp = stdin.read(1)
        return inp

    def get_input_shot(self):
        try:
            while 1:
                inp = self.get_input()
                if inp == 'w':
                    self._cursor_x = max(0, self._cursor_x - 1)
                if inp == 's':
                    self._cursor_x = min(LEN - 1, self._cursor_x + 1)
                if inp == 'a':
                    self._cursor_y = max(0, self._cursor_y - 1)
                if inp == 'd':
                    self._cursor_y = min(LEN - 1, self._cursor_y + 1)
                if inp == 'f':
                    return (self._cursor_x, self._cursor_y)
                if inp == 'q':
                    exit(1)
                self.print_board([], [(self._cursor_x, self._cursor_y)],
                                 bot=False, msg=POINT_INPUT_TEXT)
        except SystemExit as e:
            exit(e)

    def get_input_ship(self, ship_size):
        self.get_area(ship_size)
        msg = POINT_SHIP_INPUT_TEXT.format(ship_size=ship_size)
        try:
            while 1:
                inp = self.get_input()
                if inp == 'w':
                    self._cursor_x = max(0, self._cursor_x - 1)
                if inp == 's':
                    if self._dirr == 'y':
                        self._cursor_x = min(LEN - ship_size, self._cursor_x + 1)
                    else:
                        self._cursor_x = min(LEN - 1, self._cursor_x + 1)
                if inp == 'a':
                    self._cursor_y = max(0, self._cursor_y - 1)
                if inp == 'd':
                    if self._dirr == DIRR[0]:
                        self._cursor_y = min(LEN - ship_size, self._cursor_y + 1)
                    else:
                        self._cursor_y = min(LEN - 1, self._cursor_y + 1)
                if inp == 'q':
                    exit(1)
                if inp == 'c':
                    for ship_size in SHIPS_COUNT:
                        amount = self._board_player.ships_amount(int(ship_size))
                        count = SHIPS_COUNT[ship_size] - amount
                        for _ in range(count):
                            while 1:
                                point = self.get_random_point()
                                dirr = choice(DIRR)
                                if self._board_player.set_ship(Ship(point, int(ship_size), dirr)):
                                    break
                    raise errors.RandomSet()
                if inp == 'r':
                    try:
                        self.toggle_dirr()
                        self.get_area(ship_size)
                    except errors.RotateError:
                        self.toggle_dirr()
                        print(ROTATION_ERROR_TEXT, end='\r')
                        continue
                    self.print_board(self._area, [], bot=True, msg=msg)
                    continue
                if inp == 'f':
                    return Ship((self._cursor_x, self._cursor_y), ship_size,
                                self._dirr)

                self.get_area(ship_size)
                self.print_board(self._area, [], bot=True, msg=msg)
        except SystemExit as e:
            exit(e)

    def print_board(self, player_squares=[],
                    bot_squares=[], bot=True, msg=None):
        if name == 'nt':
            system('cls')
        else:
            system('clear')

        top_line = ' '*2
        for i in range(LEN):
            top_line += self.add_whitespace(i)
        print(self.add_indent(top_line))

        board_player = self._board_player.get_board()
        board_bot = self._board_bot.get_board(True)
        for x in range(LEN):
            board_player_line = self.add_whitespace(ALPHABET[x])
            board_bot_line = self.add_whitespace(ALPHABET[x])
            for y in range(LEN):
                if bot:
                    if (x, y) not in player_squares:
                        board_player_line += self.add_whitespace(board_player[x][y])
                    else:
                        if (x, y) in self._board_player.get_area():
                            board_player_line += self.add_whitespace(LEGEND['cursor_ship'])
                        else:
                            board_player_line += self.add_whitespace(LEGEND['cursor'])
                    board_bot_line += self.add_whitespace(board_bot[x][y])
                else:
                    board_player_line += self.add_whitespace(board_player[x][y])
                    if (x, y) in bot_squares:
                        if (x, y) in self._board_bot.get_damaged_units():
                            board_bot_line += self.add_whitespace(LEGEND['cursor_damaged_ship'])
                        elif (x, y) in self._board_bot.get_checked_squares():
                            board_bot_line += self.add_whitespace(LEGEND['cursor_miss'])
                        else:
                            board_bot_line += self.add_whitespace(LEGEND['cursor'])
                    else:
                        board_bot_line += self.add_whitespace(board_bot[x][y])
            print(self.add_indent(board_player_line, board_bot_line))
        if msg:
            print(msg)

    def play(self):
        if name != 'nt':
            orig_settings = termios.tcgetattr(stdin)
            tty.setcbreak(stdin)
        try:
            self.set_ships()
            self.set_random_ships()
            self.print_board()
            while 1:
                try:
                    self.shot_player()
                except errors.GameOver:
                    print(WIN_MSG)
                    break
                try:
                    self.shot_bot()
                except errors.GameOver:
                    print(LOSE_MSG)
                    break
                self.print_board()
        except KeyboardInterrupt as e:
            exit(e)
        finally:
            if name != 'nt':
                termios.tcsetattr(stdin, termios.TCSADRAIN, orig_settings)
