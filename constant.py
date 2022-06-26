ALPHABET = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J')
LEN = len(ALPHABET)
DIRR = ['x', 'y']
WIN_MSG = 'You won'
LOSE_MSG = 'You lost'
POINT_INPUT_TEXT = 'Choose target coorditates:\n'
UNALLOWED_SHOT_TARDET = 'Unallowed shot target, try again'
POINT_SHIP_INPUT_TEXT = 'WASD to move ship\nR to rotate by 90 degrees\nF to select position\nQ to quit\nEnter a {ship_size}-unit ship coorditates:\n'
ROTATION_ERROR_TEXT = 'Unable to rotate, try other position'
SHIP_UNALLOWED_POSITION = 'Unallowed position, ships are too close'
INDENT_WIDTH = 3
SHIPS_COUNT = {
    '4': 1,
    '3': 2,
    '2': 3,
    '1': 4,
}
LEGEND = {
    'empty_cell': ' ',
    'miss': '•',  # alt + 7
    'ship': '■',  # alt + 254
    'damaged_ship': '○',  # alt + 9
    'destroyed_ship': 'x',
    'coursor_ship': '◙',  # alt + 10
    'coursor': 'o',
    'coursor_miss': '⊙',
    'coursor_damaged_ship': 'ⓧ'
}
