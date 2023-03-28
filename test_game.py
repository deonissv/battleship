from game import Game
from pytest import raises
from errors import TestError


def test_get_input_point_too_long(monkeypatch):

    def inp_text(*args):
        return 'asd'

    def return_text(text):
        raise TestError()

    monkeypatch.setattr('game.Game.get_input', inp_text)
    monkeypatch.setattr('builtins.print', return_text)
    game = Game()
    with raises(TestError):
        game.get_input_shot()


def test_get_input_point_too_short(monkeypatch):
    def inp_text(*args):
        return 'a'

    def return_text(text):
        raise TestError()

    monkeypatch.setattr('game.Game.get_input', inp_text)
    monkeypatch.setattr('builtins.print', return_text)
    game = Game()
    with raises(TestError):
        game.get_input_shot()


def test_get_input_point_invalid_letter(monkeypatch):
    def inp_text(*args):
        return 'z1'

    def return_text(text):
        raise TestError()

    monkeypatch.setattr('game.Game.get_input', inp_text)
    monkeypatch.setattr('builtins.print', return_text)
    game = Game()
    with raises(TestError):
        game.get_input_shot()


def test_get_input_point_not_a_number(monkeypatch):
    def return_text(text):
        raise TestError()

    monkeypatch.setattr('game.Game.get_input', return_text)
    monkeypatch.setattr('builtins.print', return_text)
    game = Game()
    with raises(TestError):
        game.get_input_shot()


def test_get_input_point_typical(monkeypatch):
    def inp_text(*args):
        return 'f'

    monkeypatch.setattr('game.Game.get_input', inp_text)
    game = Game()
    assert game.get_input_shot() == (0, 0)


def test_add_indent():
    game = Game()
    assert game.add_indent('123') == '123   |   123'
    assert game.add_indent('123', '234') == '123   |   234'


def test_add_whitespace():
    game = Game()
    assert game.add_whitespace('asd') == 'asd '
