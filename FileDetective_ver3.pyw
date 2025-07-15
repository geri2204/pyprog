import os
import tkinter as tk
from tkinter import ttk, messagebox
from watchdog.observers import Observer
from datetime import datetime
from watchdog.events import FileSystemEventHandler

# Watchdog event handler
class BeerkezettEventHandler(FileSystemEventHandler):
    def __init__(self, indicator, refresh_files_callback, mini_indicator):
        self.indicator = indicator
        self.refresh_files_callback = refresh_files_callback
        self.mini_indicator = mini_indicator

    def on_any_event(self, event):
        self.indicator.config(bg='green')
        self.mini_indicator.config(bg='green')
        self.indicator.after(5000, lambda: self.indicator.config(bg='red'))
        self.mini_indicator.after(5000, lambda: self.mini_indicator.config(bg='red'))
        self.refresh_files_callback()

def list_files_in_directory(directory):
    file_list = []
    beerkezett_files = {}
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            modification_time = os.path.getmtime(full_path)
            file_list.append((root, file, modification_time))
            if "Beerkezett" in root:
                if root not in beerkezett_files:
                    beerkezett_files[root] = []
                beerkezett_files[root].append(file)
    
    # Rendezés módosítási idő szerint csökkenő sorrendben
    file_list.sort(key=lambda x: x[2], reverse=True)
    
    # Csak az utolsó 10 fájl kiválasztása
    file_list = file_list[:10]
    
    return file_list, beerkezett_files

def display_files():
    directory = directory_entry.get()
    if not os.path.isdir(directory):
        messagebox.showerror("Error", "The specified path is not a directory or does not exist.")
        return

    files, beerkezett_files = list_files_in_directory(directory)
    all_files_textbox.delete(1.0, tk.END)
    beerkezett_files_textbox.delete(1.0, tk.END)
    
    if not files:
        all_files_textbox.insert(tk.END, "No files found.")
    else:
        for file_info in files:
            dt_object=datetime.fromtimestamp(file_info[2]);
            formatted_time=dt_object.strftime('%Y-%m-%d %H:%M:%S');
            all_files_textbox.insert(tk.END, f"Directory: {file_info[0]}, \n\t\t\t\t\t\t\t\t\t⌊ File: {file_info[1]} (Modified: {formatted_time})\n")
    
    if not beerkezett_files:
        beerkezett_files_textbox.insert(tk.END, "No files found in 'Beerkezett' directories.")
    else:
        for dir_path, files in beerkezett_files.items():
            beerkezett_files_textbox.insert(tk.END, f"Directory: {dir_path}\n")
            for file in files:
                
                beerkezett_files_textbox.insert(tk.END, f"\t\t\t\t\t\t\t\t\t⌊ File: {file}\n")
    
    # Update the Beerkezett file count
    beerkezett_count_label.config(text=f"Beérkezett: {sum(len(files) for files in beerkezett_files.values())}")
    mini_beerkezett_count_label.config(text=f"Beérkezett: {sum(len(files) for files in beerkezett_files.values())}")
    
    # Start watching Beerkezett directories
    start_watching_beerkezett(beerkezett_files)

def start_watching_beerkezett(beerkezett_files):
    global observer

    if observer:
        observer.stop()
        observer.join()

    observer = Observer()
    event_handler = BeerkezettEventHandler(indicator, lambda: refresh_beerkezett_files(beerkezett_files), mini_indicator)

    for directory in beerkezett_files.keys():
        observer.schedule(event_handler, directory, recursive=True)
    
    observer.start()

def refresh_beerkezett_files(beerkezett_files):
    directory = directory_entry.get()
    files, new_beerkezett_files = list_files_in_directory(directory)
    
    beerkezett_files_textbox.delete(1.0, tk.END)
    
    if not new_beerkezett_files:
        beerkezett_files_textbox.insert(tk.END, "No files found in 'Beerkezett' directories.")
    else:
        for dir_path, files in new_beerkezett_files.items():
            beerkezett_files_textbox.insert(tk.END, f"Directory: {dir_path}\n")
            for file in files:
                beerkezett_files_textbox.insert(tk.END, f"\t\t\t\t\t\t\t\t\t⌊ File: {file}\n")
    
    # Update the Beerkezett file count
    beerkezett_count_label.config(text=f"Beérkezett: {sum(len(files) for files in new_beerkezett_files.values())}")
    mini_beerkezett_count_label.config(text=f"Beérkezett: {sum(len(files) for files in new_beerkezett_files.values())}")

# GUI setup
root = tk.Tk()
root.title("File Detective")

mainframe = ttk.Frame(root, padding="10 10 10 10")
mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

directory_label = ttk.Label(mainframe, text="Vizsgálandó mappa útvonala:")
directory_label.grid(row=0, column=0, sticky=tk.W)

options = ['Z:\\Alkalmazasok\\ÉMÁSZ SAP\\prod\\emaszAmb\\adatcsere2_atm']
selected_option = tk.StringVar()
directory_entry = ttk.Combobox(mainframe, textvariable=selected_option, values=options, width=180)
directory_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
directory_entry['state'] = 'normal'

list_files_button = ttk.Button(mainframe, text="LISTÁZÁS", command=display_files)
list_files_button.grid(row=0, column=2, sticky=tk.W)

all_files_label = ttk.Label(mainframe, text="Összes fájl listája:")
all_files_label.grid(row=1, column=0, columnspan=3, sticky=tk.W)

all_files_textbox = tk.Text(mainframe, width=80, height=10)
all_files_textbox.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E))

beerkezett_files_label = ttk.Label(mainframe, text="Fájlok a 'Beerkezett' mappában:")
beerkezett_files_label.grid(row=3, column=0, columnspan=3, sticky=tk.W)

beerkezett_files_textbox = tk.Text(mainframe, width=180, height=20)
beerkezett_files_textbox.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))

beerkezett_count_label = ttk.Label(mainframe, text="A 'Beerkezett' mappában ennyi fájl van: 0")
beerkezett_count_label.grid(row=5, column=0, sticky=tk.W)

indicator_label = ttk.Label(mainframe, text="A 'Beerkezett' mappa aktivitása:")
indicator_label.grid(row=6, column=0, sticky=tk.W)

indicator = tk.Label(mainframe, bg='red', width=2, height=1)
indicator.grid(row=6, column=1, sticky=tk.W)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=1)

# Mini window setup
mini_window = tk.Toplevel(root)
mini_window.geometry("100x30+1435+60")
mini_window.overrideredirect(True)
mini_window.attributes("-topmost", True)
mini_window.attributes("-alpha", 0.7)

mini_frame = ttk.Frame(mini_window, padding="5 5 5 5")
mini_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

mini_indicator = tk.Label(mini_frame, bg='red', width=2, height=1)
mini_indicator.grid(row=0, column=0, sticky=tk.W)

mini_beerkezett_count_label = ttk.Label(mini_frame, text="Beérkezett: 0")
mini_beerkezett_count_label.grid(row=0, column=1, sticky=tk.W)



observer = None

try:
    root.mainloop()
finally:
    if observer:
        observer.stop()
        observer.join()
