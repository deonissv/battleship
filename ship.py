from errors import InvalidDirr, InvalidSize
from constant import SHIPS_COUNT, LEN


class Ship:

    def __init__(self, point, size, dirr):
        self._x, self._y = point
        if size not in [int(key) for key in SHIPS_COUNT.keys()]:
            raise InvalidSize()
        self._size = size
        self._hp = size
        if dirr not in ('x', 'y'):
            raise InvalidDirr()
        self._dirr = dirr
        self._damaged_units = set()
        self._area = set()
        if dirr == 'x':
            for i in range(self._size):
                self._area.add((self._x, self._y + i))
        if dirr == 'y':
            for i in range(self._size):
                self._area.add((self._x + i, self._y))
        self._surroundings = set()
        for x, y in self._area:
            self._surroundings.update([(x, y+1), (x, y-1), (x-1, y+1),
                                       (x-1, y-1), (x+1, y+1), (x+1, y-1),
                                       (x+1, y), (x-1, y)])
        self._surroundings = self._surroundings - set(self._area)
        for x, y in self._surroundings:
            res = self._surroundings.copy()

            if not (-1 < x and x < LEN) or not (-1 < y and y < LEN):
                res.remove((x, y))
            self._surroundings = res

    def get_size(self):
        """
        Returns a size value
        """
        return self._size

    def get_dirr(self):
        """
        Returns a dirr value
        """
        return self._dirr

    def get_area(self):
        """
        Returns a set of squares that are occupied by a ship
        """
        return self._area

    def get_surroundings(self):
        """
        Returns a set of squares that borders on a area of a ship
        """
        return self._surroundings

    def get_damaged_units(self):
        """
        Returns a set of damaged units
        """
        return self._damaged_units

    def get_unavailable_squares(self):
        """
        Returns a set of squares that cannot be chosen as a target
        """
        if self.is_alive():
            return self._damaged_units
        else:
            return self._area | self._surroundings

    def is_alive(self):
        """
        Checks if a ship is alive
        """
        return self._hp > 0

    def add_damaged_unit(self, point):
        """
        Adds a new unit to self._damaged_units and decreases a hp value
        """
        if point in self._area:
            self._hp -= 1
            self._damaged_units.add(point)

    def check_hit(self, point):
        """
        Checks if the shot hit a ship
        Returns True if has hit, otherwise False
        """
        if point in self._area - self._damaged_units:
            self.add_damaged_unit(point)
            return True
        return False
