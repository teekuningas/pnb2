""" Contains input methods
"""
import keyboard


def get_inputs():
    """ Transforms keyboard events to actions
    """
    actions = []
    if keyboard.is_pressed('left'):
        actions.append('MOVE_LEFT')

    if keyboard.is_pressed('right'):
        actions.append('MOVE_RIGHT')

    if keyboard.is_pressed('up'):
        actions.append('MOVE_UP')

    if keyboard.is_pressed('down'):
        actions.append('MOVE_DOWN')
    return actions

