import tkinter as tk
from tkinter import ttk 
from tkinter import simpledialog, filedialog
from PIL import Image, ImageTk
import configparser
import os
import PIL


def show_ini_content(ini_file_path):
    # INI-datei öffnen und Inhalt auslesen
    config = configparser.ConfigParser()
    config.read(ini_file_path)

    # wrte aus der INI-Datei auslesen
    kommazahlen = config.get('Settings', 'Kommazahlen')
    art = config.get('Settings', 'Art')
    koordination = config.get('Settings', 'Koordination')
    rotation = config.get('Settings', 'Rotation')
    esp32bild = config.get('Settings', 'esp32bild')
    lokalesbild = config.get('Settings', 'lokalesbild')
    croppedbild = config.get('Settings', 'Croppedbild')
  


    # neue GUI für die Anzeige der INI-Inhalte erstellen
    display_window = tk.Toplevel()
    display_window.title("INI-Inhalte anzeigen")

    # funktion zum erstellen von labels in fett und rot
    def create_bold_red_label(text):
        return tk.Label(display_window, text=text, font=('Helvetica', 10, 'bold'), fg='red')

    # funktion zum speichern von kommazahlen in der INI-Datei
    def save_kommazahlen():
        new_kommazahlen = simpledialog.askstring("Kommazahlen", "Bitte geben Sie den Wert für die Kommazahlen ein:")
        if new_kommazahlen is not None:
            config.set('Settings', 'Kommazahlen', new_kommazahlen)
            with open(ini_file_path, 'w') as configfile:
                config.write(configfile)
            update_display()  # aktualisiere anzeige

    def save_art():
        # neue GUI für die auswahl erstellen
        input_window = tk.Toplevel()
        input_window.title("ART auswählen")

        # funktion zum speichern der ausgewählten kommazahlen
        def save_selected_value():
            selected_value = combo_box.get()
            if selected_value:
                config.set('Settings', 'ART', selected_value)
                with open(ini_file_path, 'w') as configfile:
                    config.write(configfile)
                input_window.destroy()  
                update_display()  # aktualisiere anzeige

        # dropdow für die auswahl erstellen
        combo_box = ttk.Combobox(input_window, values=["gauge", "zahlen"])
        combo_box.pack(pady=10)

        # button zum speichern der auswahl erstellen
        save_button = tk.Button(input_window, text="Speichern", command=save_selected_value)
        save_button.pack(pady=5)




    # funktion zum aktualisieren der anzeige
    def update_display():
        kommazahlen_label.config(text=config.get('Settings', 'Kommazahlen'))
        koordination_label.config(text=config.get('Settings', 'Koordination'))

    # labels für die INI-Inhalte erstellen und anzeigen
    label_kommazahlen = create_bold_red_label("Kommazahlen: ")
    label_kommazahlen.pack(pady=5)
    kommazahlen_label = tk.Label(display_window, text=kommazahlen)
    kommazahlen_label.pack()

    label_art = create_bold_red_label("Art: ")
    label_art.pack(pady=5)
    art_label = tk.Label(display_window, text=art)
    art_label.pack()

    label_koordination = create_bold_red_label("Koordination: ")
    label_koordination.pack(pady=5)
    koordination_label = tk.Label(display_window, text=koordination)
    koordination_label.pack()

    label_rotation = create_bold_red_label("Rotation: ")
    label_rotation.pack(pady=5)
    tk.Label(display_window, text=rotation).pack()

    label_esp32bild = create_bold_red_label("ESP32 Bild: ")
    label_esp32bild.pack(pady=5)
    tk.Label(display_window, text=esp32bild).pack()

    label_lokalesbild = create_bold_red_label("Lokales Bild: ")
    label_lokalesbild.pack(pady=5)
    tk.Label(display_window, text=lokalesbild).pack()

    label_croppedbild = create_bold_red_label("Cropped Bild: ")
    label_croppedbild.pack(pady=5)
    tk.Label(display_window, text=croppedbild).pack()

    # button für die änderung von kommazahlen 
    kommazahlen_button = tk.Button(display_window, text="Kommazahlen ändern", command=save_kommazahlen)
    kommazahlen_button.pack(pady=5)

    # button für die änderung von der ART 
    art_button = tk.Button(display_window, text="ART ändern", command=save_art)
    art_button.pack(pady=5)

    # buttons für "Lokales Bild" und "ESP32 Bild" erstellen
    local_button = tk.Button(display_window, text="Lokales Bild", command=lambda: save_lokal_image_to_ini(ini_file_path))
    local_button.pack(pady=5)

    esp32_button = tk.Button(display_window, text="ESP32 Bild", command=lambda: save_esp32_image_to_ini(ini_file_path))
    esp32_button.pack(pady=5)

    # button "Bild drehen" 
    rotate_button = tk.Button(display_window, text="Bild drehen", command=open_rotation_file)
    rotate_button.pack(pady=5)

    # bild anzeigen, falls ein Wert für "lokalesbild" vorhanden ist
    if lokalesbild:
        try:
            image = Image.open(lokalesbild)
            image.thumbnail((400, 400))  
            photo = ImageTk.PhotoImage(image)
            image_label = tk.Label(display_window, image=photo)
            image_label.image = photo  
            image_label.pack(pady=10)
        except Exception as e:
            print("Fehler beim Laden des Bildes:", e)

def open_rotation_file():
    try:
        os.system("python3 drehen.py")
    except Exception as e:
        print("Fehler beim Öffnen von drehen.py:", e)


def load_local_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        print(f"Lokales Bild ausgewählt: {file_path}")

def save_lokal_image_to_ini(ini_file_path):
    lokal_file_path = filedialog.askopenfilename()
    if lokal_file_path:
        print(f"Lokal Bild ausgewählt: {lokal_file_path}")

        # den ausgewählten dateinamen als Wert für den schlüssel "esp32bild" in der INI-Datei speichern
        config = configparser.ConfigParser()
        config.read(ini_file_path)

        # sicherstellen, dass die sektion "Settings" vorhanden ist
        if 'Settings' not in config:
            config['Settings'] = {}

        config.set('Settings', 'lokalesbild', lokal_file_path)

        with open(ini_file_path, 'w') as configfile:
            config.write(configfile)

def save_esp32_image_to_ini(ini_file_path):
   
    esp32_bild = simpledialog.askstring("ESP32 Bild", "Bitte geben Sie den Wert für das ESP32 Bild ein:")

    if esp32_bild:
        print(f"ESP32 Bild ausgewählt: {esp32_bild}")

        # den eingegebenen wert als wert für den cchlüssel "esp32bild" in der INI-Datei speichern
        config = configparser.ConfigParser()
        config.read(ini_file_path)

        # sicherstellen, dass die Sektion "Settings" vorhanden ist
        if 'Settings' not in config:
            config['Settings'] = {}

        config.set('Settings', 'esp32bild', esp32_bild)

        with open(ini_file_path, 'w') as configfile:
            config.write(configfile)
