from pynput.keyboard import Key, Listener
from devices.keymaping import pynput_mapping


def key_to_str(key):
    try:
        key_str = key.__dict__.get('_name_', key.__dict__.get('char', {})).lower()
        # print(key_str)
        return key_str
    except AttributeError:
        print(f'Unknown key: {key.__dict__}')


class PyinputValidator:
    def __init__(self, keys, action_name):
        self.keys = keys[:1]
        self.action_name = action_name
        self.remaining_keys = set([pynput_mapping[k] for k in self.keys])

        def on_action(key):
            key_str = key_to_str(key)
            self.remaining_keys.discard(key_str)

        self.listener = Listener(on_press=on_action if self.action_name == 'press' else None,
                                 on_release=on_action if self.action_name == 'release' else None, )

        self.listener.start()

    def validate(self):
        if len(self.remaining_keys) == 0:
            print(f'111111111111111111111111111111111 {self.keys}')
        return len(self.remaining_keys) == 0

    def stop(self):
        self.listener.stop()
