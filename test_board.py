from board import Board
from ship import Ship
from errors import GameOver
from pytest import raises
from numpy import array_equal


def test_get_damaged_ship():
    board = Board()
    ship = Ship((0, 0), 2, 'x')
    ship.add_damaged_unit((0, 0))
    board.set_ship(ship)
    board.set_ship(Ship((1, 3), 1, 'x'))
    board.set_ship(Ship((5, 6), 1, 'x'))
    assert board.get_damaged_ship() == (ship, {(0, 0)})


def test_get_damaged_units():
    board = Board()
    ship = Ship((0, 0), 4, 'x')
    ship.add_damaged_unit((0, 0))
    board.set_ship(ship)
    ship = Ship((4, 0), 4, 'x')
    ship.add_damaged_unit((4, 1))
    board.set_ship(ship)
    assert board.get_damaged_units() == set(((0, 0), (4, 1)))


def test_get_area():
    board = Board()
    board.set_ship(Ship((1, 3), 2, 'x'))
    board.set_ship(Ship((5, 6), 1, 'x'))
    assert board.get_area() == {(1, 3), (1, 4), (5, 6)}


def test_get_destroyed_units():
    board = Board()
    assert board.get_destroyed_units() == set()
    ship = Ship((0, 0), 1, 'x')
    ship.add_damaged_unit((0, 0))
    board.set_ship(ship)
    ship = Ship((5, 0), 2, 'x')
    ship.add_damaged_unit((5, 0))
    ship.add_damaged_unit((5, 1))
    board.set_ship(ship)
    assert board.get_destroyed_units() == {(0, 0), (5, 0), (5, 1)}


def test_get_unavailable_squares():
    board = Board()
    assert board.get_unavailable_squares() == set()
    ship = Ship((0, 0), 1, 'x')
    ship.add_damaged_unit((0, 0))
    board.set_ship(ship)
    assert board.get_unavailable_squares() == {(0, 1), (1, 0), (1, 1), (0, 0)}
    ship = Ship((5, 0), 2, 'x')
    ship.add_damaged_unit((5, 0))
    ship.add_damaged_unit((5, 1))
    board.set_ship(ship)
    assert board.get_unavailable_squares() == {(0, 1), (6, 2), (4, 0), (0, 0),
                                               (6, 1), (1, 1), (5, 1), (4, 2),
                                               (5, 0), (6, 0), (1, 0), (4, 1),
                                               (5, 2)}


def test_get_board():
    board = Board()
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
    assert array_equal(board.get_board(), arr)
    board.set_ship(Ship((0, 0), 1, 'x'))
    arr = [['■', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
    assert array_equal(board.get_board(), arr)
    board.set_ship(Ship((5, 0), 4, 'x'))
    arr = [['■', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
           ['■', '■', '■', '■', ' ', ' ', ' ', ' ', ' ', ' '],
           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
           [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
    assert array_equal(board.get_board(), arr)


def test_set_ship_typical():
    board = Board()
    assert board.set_ship(Ship((0, 0), 4, 'x')) is True
    assert board.set_ship(Ship((4, 4), 4, 'y')) is True
    assert board.set_ship(Ship((6, 6), 2, 'x')) is True
    assert board.set_ship(Ship((2, 2), 4, 'y')) is True


def test_set_ship_ship_are_too_close():
    board = Board()
    assert board.set_ship(Ship((0, 0), 4, 'x')) is True

    assert board.set_ship(Ship((1, 0), 4, 'x')) is False
    assert board.set_ship(Ship((0, 1), 4, 'x')) is False
    assert board.set_ship(Ship((0, 0), 4, 'x')) is False
    assert board.set_ship(Ship((0, 0), 4, 'y')) is False


def test_set_ship_ship_out_of_board():
    board = Board()

    assert board.set_ship(Ship((8, 0), 4, 'y')) is False
    assert board.set_ship(Ship((7, 0), 4, 'y')) is False
    assert board.set_ship(Ship((6, 7), 4, 'x')) is False
    assert board.set_ship(Ship((9, 9), 2, 'x')) is False


def test_check_win():
    board = Board()
    ship = Ship((0, 0), 1, 'x')
    board.set_ship(ship)
    assert board.check_win() is None
    ship.add_damaged_unit((0, 0))
    with raises(GameOver):
        board.check_win()


def test_shot_hit():
    board = Board()
    board.set_ship(Ship((0, 0), 2, 'x'))
    assert board.shot((0, 0)) is True


def test_shot_miss():
    board = Board()
    board.set_ship(Ship((0, 0), 2, 'x'))
    assert board.shot((1, 0)) is False


def test_shot_invalid_target():
    board = Board()
    board.set_ship(Ship((0, 0), 1, 'x'))
    board.set_ship(Ship((5, 0), 4, 'x'))
    board.shot((0, 0))
    assert board.shot((0, 0)) is None
    assert board.shot((0, 1)) is None
    assert board.shot((1, 0)) is None
