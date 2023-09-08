#testscripte um scripte zu starten
import tkinter as tk
import subprocess

def start_aufgerufenes_skript():
    auswahl = dropdown_variable.get()
    subprocess.run(["python3", "muell/3.py", auswahl])

# gui erstellen
root = tk.Tk()
root.title("Dropdown-Menü Beispiel")

# dropdown erstellen
dropdown_variable = tk.StringVar(root)
dropdown_variable.set("wert1")  
dropdown_menu = tk.OptionMenu(root, dropdown_variable, "muell/3.jpg", "muell/weronek_gauge_1.jpg")
dropdown_menu.pack(pady=10)

# button zum starten der skripte

start_button = tk.Button(root, text="Skript starten", command=start_aufgerufenes_skript)
start_button.pack(pady=5)

root.mainloop()
