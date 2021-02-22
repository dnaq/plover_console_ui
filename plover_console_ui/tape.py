from wcwidth import wcwidth

from prompt_toolkit.widgets import TextArea, Frame

from plover import system

from .output import output_to_buffer

class Tape(Frame):
    def __init__(self) -> None:
        super().__init__(
            TextArea(focusable=False), title="Paper Tape", style="class:normal"
        )
        self._all_keys = None
        self._all_keys_filler = None

    def on_config_changed(self, update):
        if "system_name" in update:
            self._all_keys = "".join(key.strip("-") for key in system.KEYS)
            self._all_keys_filler = [" " * wcwidth(k) for k in self._all_keys]
            self._numbers = set(system.NUMBERS.values())
            self.container.width = len(self._all_keys) + 1

    def on_stroked(self, stroke):
        text = self._all_keys_filler * 1
        keys = stroke.steno_keys[:]
        if any(key in self._numbers for key in keys):
            keys.append("#")
        for key in keys:
            index = system.KEY_ORDER[key]
            text[index] = self._all_keys[index]
        output_to_buffer(self.body.buffer, "".join(text))
