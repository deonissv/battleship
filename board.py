from errors import GameOver
from constant import LEGEND, LEN
from numpy import full


class Board:
    def __init__(self):
        self._len = LEN
        self._ships = set()
        self._occupied = set()
        self._checked_squares = set()

    def ships_amount(self, ship_size):
        amount = 0
        for ship in self._ships:
            if ship_size == ship.get_size():
                amount += 1
        return amount

    def get_checked_squares(self):
        return self._checked_squares

    def get_damaged_ship(self):
        """
        Returns the first ship object and a list of damaged squares of this ship
        """
        for ship in self._ships:
            damaged_units = ship.get_damaged_units()
            if damaged_units and ship.is_alive():
                return ship, damaged_units

    def get_damaged_units(self):
        """
        Returns a set of damaged squares of all ships on a board
        """
        damaged_units = set()
        for ship in self._ships:
            damaged_units.update(ship.get_damaged_units())
        return damaged_units

    def get_area(self):
        """
        Returns a set of squares occupied by ships(no matter damaged,
            destroyed, or untouched)
        """
        area = set()
        for ship in self._ships:
            area.update(ship.get_area())
        return area

    def get_destroyed_units(self):
        """
        Returns a set of squares occupied by destroyed ships
        """
        destroyed_units = set()
        for ship in self._ships:
            if not ship.is_alive():
                destroyed_units.update(ship.get_area())
        return destroyed_units

    def get_unavailable_squares(self):
        """
        Returns a set of squares that cannot be chosen as a target
        """
        unavailable_squares = set()
        for ship in self._ships:
            unavailable_squares.update(ship.get_unavailable_squares())
        return unavailable_squares | self._checked_squares

    def get_board(self, ciphered=False):
        """
        Returns an 2D array containing a board representation
        """
        board = full((self._len, self._len), ' ')
        area = self.get_area()
        damaged_units = self.get_damaged_units()
        destroyed_units = self.get_destroyed_units()
        for x in range(self._len):
            for y in range(self._len):
                if (x, y) in self._checked_squares:
                    item = LEGEND['miss']
                elif (x, y) in destroyed_units:
                    item = LEGEND['destroyed_ship']
                elif (x, y) in damaged_units:
                    item = LEGEND['damaged_ship']
                elif (x, y) in area:
                    if ciphered:
                        item = LEGEND['empty_cell']
                    else:
                        item = LEGEND['ship']
                else:
                    item = LEGEND['empty_cell']
                board[x][y] = item
        return board

    def set_ship(self, ship):
        """
        Sets a ship on a board
        """
        for x, y in ship.get_area():
            if any([x_curr >= x_max
                    for x_curr, x_max in zip((x, y), (self._len, self._len))]):
                # raise errors.ShipOutOfBoard()
                return False
            if ship.get_area() & self._occupied:
                # raise errors.ShipsAreTooCLose()
                return False
        self._occupied.update(ship.get_surroundings() | set(ship.get_area()))
        self._ships.add(ship)
        return True

    def check_win(self):
        """
        Checks if the game has ended
        Returns True if game is over, otherwise False
        """
        if not any([ship.is_alive() for ship in self._ships]):
            raise GameOver()

    def shot(self, point):
        """
        Checks if the given point can be chosen as a target.
        Returns None if point is improper
                True if any ship was hit
                False if missed
        """
        if point in self.get_unavailable_squares():
            return None
        if not all([coord in range(self._len) for coord in point]):
            return None
        for ship in self._ships:
            # if point in ship.get_area():
            if ship.check_hit(point):
                if not ship.is_alive():
                    self._checked_squares.update(ship.get_surroundings())
                self.check_win()
                return True
        else:
            self._checked_squares.add(point)
            return False
