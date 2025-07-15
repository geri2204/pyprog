import tkinter as tk
from pynput import mouse, keyboard
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key
import threading
import time

# Globális változók
recording = False
playing = False
events = []
start_time = None

# Egér események kezelése
def on_click(x, y, button, pressed):
    if recording:
        events.append(('click', time.time() - start_time, x, y, button, pressed))

def on_scroll(x, y, dx, dy):
    if recording:
        events.append(('scroll', time.time() - start_time, x, y, dx, dy))

# Billentyű események kezelése
def on_press(key):
    global recording, playing, start_time

    if key == keyboard.KeyCode.from_char('q'):
        if not recording:
            events.clear()
            start_time = time.time()
            recording = True
            print("Rögzítés elindult.")
        else:
            recording = False
            print("Rögzítés leállítva.")

    elif key == keyboard.KeyCode.from_char('w'):
        if not playing:
            playing = True
            threading.Thread(target=play_events).start()
        else:
            playing = False
            print("Lejátszás leállítva.")

    elif recording:
        events.append(('key_press', time.time() - start_time, key))

def on_release(key):
    if recording:
        events.append(('key_release', time.time() - start_time, key))

# Lejátszás funkció
def play_events():
    global playing
    mouse_controller = MouseController()
    keyboard_controller = KeyboardController()

    while playing:
        if not events:
            break
        start_play = time.time()
        for event in events:
            if not playing:
                break
            event_type = event[0]
            delay = event[1]
            time.sleep(max(0, delay - (time.time() - start_play)))

            if event_type == 'click':
                _, _, x, y, button, pressed = event
                mouse_controller.position = (x, y)
                if pressed:
                    mouse_controller.press(button)
                else:
                    mouse_controller.release(button)

            elif event_type == 'scroll':
                _, _, x, y, dx, dy = event
                mouse_controller.position = (x, y)
                mouse_controller.scroll(dx, dy)

            elif event_type == 'key_press':
                _, _, key = event
                keyboard_controller.press(key)

            elif event_type == 'key_release':
                _, _, key = event
                keyboard_controller.release(key)

# GUI létrehozása
def start_gui():
    root = tk.Tk()
    root.title("Eseményrögzítő")
    label = tk.Label(root, text="Nyomd meg a 'Q' gombot a rögzítés indításához/leállításához.\n"
                                 "Nyomd meg a 'W' gombot a lejátszás indításához/leállításához.")
    label.pack(padx=20, pady=20)
    root.mainloop()

# Figyelők indítása
mouse_listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll)
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

mouse_listener.start()
keyboard_listener.start()

# GUI indítása
start_gui()
