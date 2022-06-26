from ship import Ship
from pytest import raises
from errors import InvalidDirr, InvalidSize


def test_invalid_dirr():
    with raises(InvalidDirr):
        Ship((0, 0), 1, 'z')


def test_invalid_size():
    with raises(InvalidSize):
        Ship((0, 0), 0, 'z')


def test_get_surroundings():
    ship = Ship((0, 0), 2, 'x')
    assert ship.get_surroundings() == {(0, 2), (1, 2), (1, 0), (1, 1)}


def test_get_unavailable_squares():
    ship = Ship((0, 0), 2, 'x')
    assert ship.get_unavailable_squares() == set()
    ship.add_damaged_unit((0, 0))
    assert ship.get_unavailable_squares() == {(0, 0)}
    ship.add_damaged_unit((0, 1))
    assert ship.get_unavailable_squares() == {(0, 1), (0, 2), (1, 2), (0, 0),
                                              (1, 0), (1, 1)}


def test_is_alive():
    ship = Ship((0, 0), 4, 'x')
    ship.add_damaged_unit((0, 0))
    assert ship.is_alive() is True
    ship = Ship((0, 0), 1, 'x')
    ship.add_damaged_unit((0, 0))
    assert ship.is_alive() is False


def test_add_damaged_unit():
    ship = Ship((0, 0), 4, 'x')
    ship.add_damaged_unit((0, 0))
    assert ship.get_damaged_units() == {(0, 0)}


def test_check_hit():
    ship = Ship((0, 0), 4, 'x')
    assert ship.check_hit((0, 0)) is True
