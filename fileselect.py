import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os

def browse_source_dir():
    path = filedialog.askdirectory()
    if path:
        source_dir_var.set(path)

def browse_target_dir():
    path = filedialog.askdirectory()
    if path:
        target_dir_var.set(path)

def browse_file_list():
    path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if path:
        file_list_var.set(path)

def copy_files():
    source_dir = source_dir_var.get()
    target_dir = target_dir_var.get()
    file_list_path = file_list_var.get()

    if not (source_dir and target_dir and file_list_path):
        messagebox.showerror("Hiba", "Kérlek, válassz ki minden szükséges mappát és fájlt.")
        return

    try:
        with open(file_list_path, "r", encoding="utf-8") as f:
            file_names = [line.strip() for line in f if line.strip()]

        copied = 0
        missing = []

        for file_name in file_names:
            source_file = os.path.join(source_dir, file_name)
            if os.path.exists(source_file):
                shutil.copy2(source_file, os.path.join(target_dir, file_name))
                copied += 1
            else:
                missing.append(file_name)

        message = f"{copied} fájl sikeresen másolva."
        if missing:
            message += f"\n{len(missing)} fájl nem található:\n" + "\n".join(missing[:10])
            if len(missing) > 10:
                message += f"\n...és még {len(missing) - 10} fájl."

        messagebox.showinfo("Kész", message)

    except Exception as e:
        messagebox.showerror("Hiba", f"Hiba történt: {e}")

# GUI setup
root = tk.Tk()
root.title("Fájlmásoló lista alapján")

# Változók
source_dir_var = tk.StringVar()
target_dir_var = tk.StringVar()
file_list_var = tk.StringVar()

# Elrendezés
tk.Label(root, text="Forrás mappa:").grid(row=0, column=0, sticky="e")
tk.Entry(root, textvariable=source_dir_var, width=50).grid(row=0, column=1)
tk.Button(root, text="Tallózás", command=browse_source_dir).grid(row=0, column=2)

tk.Label(root, text="Cél mappa:").grid(row=1, column=0, sticky="e")
tk.Entry(root, textvariable=target_dir_var, width=50).grid(row=1, column=1)
tk.Button(root, text="Tallózás", command=browse_target_dir).grid(row=1, column=2)

tk.Label(root, text="Lista fájl (.txt):").grid(row=2, column=0, sticky="e")
tk.Entry(root, textvariable=file_list_var, width=50).grid(row=2, column=1)
tk.Button(root, text="Tallózás", command=browse_file_list).grid(row=2, column=2)

tk.Button(root, text="Másolás indítása", command=copy_files, bg="lightgreen").grid(row=3, column=1, pady=10)

root.mainloop()
