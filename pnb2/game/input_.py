""" Contains input methods
"""
import threading
from pynput.keyboard import Key
from pynput.keyboard import Listener
from pynput.keyboard import KeyCode


class PynputKeyboard:
    def __init__(self):
        """
        """
        self.key_status = {}

        self.listener = Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        self.listener.daemon = False
        self.listener.start()

    def shutdown(self):
        # self.listener.stop hangs sometimes so use a fix:
        if self.listener._running:
            self.listener._running = False
            self.listener._queue.put(None)
            # this might only work for linux, so must check this out for windows!!!
            # if not hasattr(self.listener, '_context'):
            #     self.listener.wait()
            # try:
            #     self.listener._display_stop.record_disable_context(
            #         self.listener._context)
            # except:
            #     pass

    def on_press(self, key):
        self.key_status[key] = True

    def on_release(self, key):
        self.key_status[key] = False

    def get_inputs(self, bind_key):
        """
        """
        actions = []
        if bind_key == 'keyboard_left':
            movements = []
            if self.key_status.get(KeyCode.from_char('a')):
                movements.append('CONTROLLED_MOVE_LEFT')
            elif self.key_status.get(KeyCode.from_char('d')):
                movements.append('CONTROLLED_MOVE_RIGHT')
            else:
                movements.append('CONTROLLED_MOVE_LEFTRIGHT_STOP')

            if self.key_status.get(KeyCode.from_char('w')):
                movements.append('CONTROLLED_MOVE_UP')
            elif self.key_status.get(KeyCode.from_char('s')):
                movements.append('CONTROLLED_MOVE_DOWN')
            else:
                movements.append('CONTROLLED_MOVE_UPDOWN_STOP')
            actions.extend(movements)

        elif bind_key == 'keyboard_right':
            movements = []
            if self.key_status.get(Key.left):
                movements.append('CONTROLLED_MOVE_LEFT')
            elif self.key_status.get(Key.right):
                movements.append('CONTROLLED_MOVE_RIGHT')
            else:
                movements.append('CONTROLLED_MOVE_LEFTRIGHT_STOP')
            if self.key_status.get(Key.up):
                movements.append('CONTROLLED_MOVE_UP')
            elif self.key_status.get(Key.down):
                movements.append('CONTROLLED_MOVE_DOWN')
            else:
                movements.append('CONTROLLED_MOVE_UPDOWN_STOP')
            actions.extend(movements)
        return actions


def initialize():
    pynput_keyboard = PynputKeyboard()
    return pynput_keyboard


if __name__ == '__main__':
    """
    """
    pk = initialize()
    while True:
        print(pk.get_inputs('keyboard_left'))
