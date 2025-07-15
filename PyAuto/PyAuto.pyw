import tkinter as tk
import tkinter.ttk as ttk
from pynput import mouse, keyboard
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key
from tkinter import filedialog, messagebox
from CommandProccess import CommandProccess
import threading
import time
import os

# Globális változók
recording = False
playing = False
events = []
start_time = None
cp = CommandProccess()
control_keys = {Key.f7, Key.f8, Key.f9, Key.f10}  # ne kerüljön mentésbe


# Ikon globálisok
mini_window = None
mini_indicator_canvas = None
warning_icon = None
default_icon = None
record_icon = None

# Egér események kezelése
def on_click(x, y, button, pressed):
    if recording:
        events.append(('click', time.time() - start_time, x, y, button, pressed))

def on_scroll(x, y, dx, dy):
    if recording:
        events.append(('scroll', time.time() - start_time, x, y, dx, dy))

# Billentyű események kezelése
def on_press(key):
    global recording, playing, start_time, events

    if key == Key.f7:
        if not recording:
            events.clear()
            start_time = time.time()
            recording = True
            print("Rögzítés elindult.")
        else:
            recording = False
            print("Rögzítés leállítva.")
            cp.save_events(events)
        update_indicator()

    elif key == Key.f8:
        if not events:
            messagebox.showwarning("Nincs esemény!", "Előbb tölts be, vagy rögzíts egy rögzített eseményfájlt a lejátszáshoz!")
            return
        if not playing:
            playing = True
            threading.Thread(target=play_events, daemon=True).start()
            print("Lejátszás elindult.")
        else:
            playing = False
            print("Lejátszás leállítva.")
        update_indicator()

    elif key == Key.f9:
        print("Kilépés...")
        os._exit(0)

    elif key == Key.f10:
        # Tallózó ablak megjelenítése
        selected_file = filedialog.askopenfilename(
            initialdir=cp.folder,
            title="Válassz betöltendő eseményfájlt",
            filetypes=(("Szövegfájlok", "*.txt"), ("Minden fájl", "*.*"))
        )
        if selected_file:
            loaded_events = cp.load_events(selected_file)
            if loaded_events:
                events.clear()
                events.extend(loaded_events)
                print(f"Események betöltve: {selected_file}")
            else:
                print("Nem sikerült betölteni az eseményeket.")

    elif recording and key not in control_keys:
        events.append(('key_press', time.time() - start_time, key))

def on_release(key):
    if recording and key not in control_keys:
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

# Ikon frissítés mindig az aktuális állapot szerint
def update_indicator():
    if recording:
        current_image = record_icon
    elif playing:
        current_image = warning_icon
    else:
        current_image = default_icon

    if mini_indicator_canvas is not None:
        mini_indicator_canvas.delete("all")
        mini_indicator_canvas.create_image(12, 12, image=current_image)

# GUI létrehozása
def start_gui():
    global mini_window, mini_indicator_canvas
    global warning_icon, default_icon, record_icon

    mini_window = tk.Tk()
    screen_width = mini_window.winfo_screenwidth()
    window_width = 280
    window_height = 40
    x = (screen_width // 2) - (window_width // 2)
    y = 0
    mini_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    mini_window.overrideredirect(True)
    mini_window.attributes("-topmost", True)
    mini_window.attributes("-alpha", 0.8)

    mini_frame = ttk.Frame(mini_window, padding="5 5 5 5")
    mini_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Képek betöltése és kicsinyítése (mind 500x500-as eredetileg)
    warning_icon = tk.PhotoImage(file="res/warning_icon.png").subsample(18, 18)
    default_icon = tk.PhotoImage(file="res/icon.png").subsample(18, 18)
    record_icon = tk.PhotoImage(file="res/recording_icon.png").subsample(18, 18)


    # Vászon az ikonhoz
    mini_indicator_canvas = tk.Canvas(mini_frame, width=24, height=24, highlightthickness=0)
    mini_indicator_canvas.grid(row=0, column=0, sticky=tk.W)
    mini_indicator_canvas.create_image(12, 12, image=default_icon)

    # Szöveg
    mini_label = ttk.Label(
        mini_frame,
        text="F7: Rögzítés indítás/leállítás; F10: Tallózás \nF8: Lejátszás indítás/leállítás; F9: Kilépés",
    )
    mini_label.grid(row=0, column=1, sticky=tk.W)

    mini_window.mainloop()

# Figyelők indítása
mouse_listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll)
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

mouse_listener.start()
keyboard_listener.start()

# GUI indítása
start_gui()
