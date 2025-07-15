import json
import os

class CommandProccess:
    def __init__(self, folder="records"):
        self.folder = folder
        os.makedirs(self.folder, exist_ok=True)

    def get_next_filename(self):
        i = 1
        while True:
            filename = f"recorded_commands_{i}.txt"
            path = os.path.join(self.folder, filename)
            if not os.path.exists(path):
                return path
            i += 1

    def _serialize_event(self, event):
        # Minden event tuple → list és konverzió (Key/Button/char) → string
        event = list(event)
        if event[0] == "click":
            # event = ('click', time, x, y, button_obj, pressed)
            event[4] = self._serialize_button(event[4])
        elif event[0] in ("key_press", "key_release"):
            # event = ('key_press', time, key_obj)
            event[2] = self._serialize_key(event[2])
        return event

    def _serialize_key(self, key):
        # Key objektum vagy char → string formátum:
        try:
            from pynput.keyboard import Key
            if hasattr(key, "name"):  # pl. Key.enter
                return f"Key.{key.name}"
            elif isinstance(key, str):
                return key
            elif hasattr(key, "char"):  # pl. KeyCode
                return repr(key.char)  # "'a'"
            else:
                return str(key)
        except ImportError:
            return str(key)

    def _serialize_button(self, button):
        # Button objektum → string
        try:
            from pynput.mouse import Button
            if hasattr(button, "name"):
                return f"Button.{button.name}"
            else:
                return str(button)
        except ImportError:
            return str(button)

    def save_events(self, events):
        serialized_events = [self._serialize_event(ev) for ev in events]
        path = self.get_next_filename()
        with open(path, "w", encoding="utf-8") as file:
            json.dump(serialized_events, file, ensure_ascii=False, indent=2)
        print(f"Események elmentve: {path}")

    def load_events(self, path):
        try:
            with open(path, "r", encoding="utf-8") as file:
                events = json.load(file)
            return [self._deserialize_event(ev) for ev in events]
        except Exception as e:
            print(f"Hiba a betöltés során: {e}")
            return []

    def _deserialize_event(self, event):
        # Rekonstruáljuk a Key/Button típusokat, ahol kell
        event = list(event)
        if event[0] == "click":
            event[4] = self._deserialize_button(event[4])
        elif event[0] in ("key_press", "key_release"):
            event[2] = self._deserialize_key(event[2])
        return event

    def _deserialize_key(self, key_repr):
        from pynput.keyboard import Key
        # "'a'" → karakter, "Key.enter" → Key.enter
        if isinstance(key_repr, str):
            if key_repr.startswith("'") and key_repr.endswith("'") and len(key_repr) == 3:
                return key_repr[1]
            elif key_repr.startswith("Key."):
                key_name = key_repr[4:]
                if hasattr(Key, key_name):
                    return getattr(Key, key_name)
            else:
                return key_repr
        return key_repr

    def _deserialize_button(self, btn_repr):
        from pynput.mouse import Button
        # "Button.left" → Button.left
        if isinstance(btn_repr, str) and btn_repr.startswith("Button."):
            btn_name = btn_repr[7:]
            if hasattr(Button, btn_name):
                return getattr(Button, btn_name)
        return btn_repr
