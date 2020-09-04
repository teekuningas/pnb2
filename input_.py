""" Contains input methods
"""
import keyboard


def get_inputs(bind_key):
    """ Transforms keyboard events to actions
    """
    actions = []
    if bind_key == 'keyboard_left':
        movements = []
        if keyboard.is_pressed('a'):
            movements.append('CONTROLLED_MOVE_LEFT')
        if keyboard.is_pressed('d'):
            movements.append('CONTROLLED_MOVE_RIGHT')
        if keyboard.is_pressed('w'):
            movements.append('CONTROLLED_MOVE_UP')
        if keyboard.is_pressed('s'):
            movements.append('CONTROLLED_MOVE_DOWN')
        if not movements:
            movements.append('CONTROLLED_MOVE_STOP')
        actions.extend(movements)

    elif bind_key == 'keyboard_right':
        movements = []
        if keyboard.is_pressed('left'):
            movements.append('CONTROLLED_MOVE_LEFT')
        if keyboard.is_pressed('right'):
            movements.append('CONTROLLED_MOVE_RIGHT')
        if keyboard.is_pressed('up'):
            movements.append('CONTROLLED_MOVE_UP')
        if keyboard.is_pressed('down'):
            movements.append('CONTROLLED_MOVE_DOWN')
        if not movements:
            movements.append('CONTROLLED_MOVE_STOP')
        actions.extend(movements)

    return actions

