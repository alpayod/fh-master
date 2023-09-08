import tkinter as tk
import os
from tkinter import simpledialog
import tkinter.filedialog as filedialog
from tkinter import messagebox
import configparser
import ini_viewer_gui  
from PIL import Image, ImageTk 


canvas = None

def create_scan():
    root.withdraw()  
    input_window = tk.Toplevel(root)
    input_window.title("Dateinamen eingeben")

    def save_input():
        file_name = entry.get()
        if file_name:
            save_input_to_ini(file_name)
            input_window.destroy()
            root.deiconify()  
            update_dropdown_options()

    label = tk.Label(input_window, text="Bitte geben Sie den Dateinamen ein:")
    label.pack(pady=5)

    entry = tk.Entry(input_window)
    entry.pack(pady=5)

    save_button = tk.Button(input_window, text="Speichern", command=save_input)
    save_button.pack(pady=10)

def save_input_to_ini(file_name):
    ini_folder = "ini"
    if not os.path.exists(ini_folder):
        os.makedirs(ini_folder)

    file_path = os.path.join(ini_folder, f"{file_name}.ini")

    config = configparser.ConfigParser()
    config.add_section('Settings') 
    config.set('Settings', 'Name', file_name)
    config.set('Settings', 'Kommazahlen', '0')  
    config.set('Settings', 'Koordination', '0')
    config.set('Settings', 'Rotation', '0')
    config.set('Settings', 'esp32bild', '')  
    config.set('Settings', 'lokalesbild', '')
    config.set('Settings', 'croppedbild', '')
    config.set('Settings', 'art', '')
    config.set('Settings', 'min_angle', '0')
    config.set('Settings', 'max_angle', '0')
    config.set('Settings', 'min_value', '0')
    config.set('Settings', 'max_value', '0')

    with open(file_path, 'w') as configfile:
        config.write(configfile)

    print(f"Eingabe wurde in {file_path} gespeichert.")

def update_dropdown_options():
    ini_folder = "ini"
    if not os.path.exists(ini_folder):
        return

    # alle ini datein abrufen
    ini_files = [f.replace(".ini", "") for f in os.listdir(ini_folder) if f.endswith(".ini")]

    # dropdown akualisieren
    dropdown_menu["menu"].delete(0, "end")
    for file_name in ini_files:
        dropdown_menu["menu"].add_command(label=file_name, command=lambda value=file_name: dropdown_var.set(value))


def edit_scan():
    selected_option = dropdown_var.get()
    if selected_option and selected_option != "Bitte wählen":
        ini_file_path = os.path.join("ini", f"{selected_option}.ini")
        print(f"Scan '{selected_option}' wird bearbeitet... (Dateipfad: {ini_file_path})")

        ini_viewer_gui.show_ini_content(ini_file_path)  

    else:
        messagebox.showwarning("Achtung", "Bitte wählen Sie eine INI-Datei aus.")

# GUI 
root = tk.Tk()
root.title("Scan-Ersteller")
root.geometry("500x500")  

# dropdown erstellen
dropdown_var = tk.StringVar(root)
dropdown_var.set("Bitte wählen")  
dropdown_menu = tk.OptionMenu(root, dropdown_var, "Bitte wählen")
dropdown_menu.pack(pady=10)


def rotieren_function():
    selected_option = dropdown_var.get()
    if selected_option and selected_option != "Bitte wählen":
        ini_file_path = os.path.join("ini", f"{selected_option}.ini")
        print(f"Scan '{selected_option}' wird rotiert... (Dateipfad: {ini_file_path})")

        # ini und bild lesen
        config = configparser.ConfigParser()
        config.read(ini_file_path)
        lokalesbild_value = config.get('Settings', 'lokalesbild')

        # lokales bild anzeigen
        print(f"Der Wert für 'lokalesbild' ist: {lokalesbild_value}")

        # lokalesbild in gui öffnen
        open_image_gui(lokalesbild_value)

    else:
        messagebox.showwarning("Achtung", "Bitte wählen Sie eine INI-Datei aus.")

#default rotation ist 0
def open_image_gui(image_path, rotation_angle=0):  
    global canvas
    if os.path.exists(image_path):
        image_win = tk.Toplevel(root)
        image_win.title("Bild anzeigen")

        # urspüngliches bild öffnen
        original_image_pil = Image.open(image_path)

        # rotationswert aus ini lesen
        selected_option = dropdown_var.get()
        if selected_option and selected_option != "Bitte wählen":
            ini_file_path = os.path.join("ini", f"{selected_option}.ini")
            config = configparser.ConfigParser()
            config.read(ini_file_path)

            # wenn ein wert vorhanden ist soll der rotationswert verwendet werden
            rotation_angle = config.getfloat('Settings', 'Rotation', fallback=0)

        # das bild nach den rotationswerten drehen
        rotated_image_pil = original_image_pil.rotate(rotation_angle, expand=True)

        
        image_tk = ImageTk.PhotoImage(rotated_image_pil)

        # canvas erstellen und bild hinzufügen
        canvas = tk.Canvas(image_win, width=900, height=900)
        canvas.pack()
        canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)

        
        canvas.original_image_pil = original_image_pil

        # rotationswinkel wird gesetzt
        canvas.rotation_angle = rotation_angle

        # buttons zum rotieren und speichern 
        rotate_left_button = tk.Button(image_win, text="Links", command=lambda: rotate_image(canvas, -0.5))
        rotate_left_button.pack(side=tk.LEFT, padx=10)

        rotate_right_button = tk.Button(image_win, text="Rechts", command=lambda: rotate_image(canvas, 0.5))
        rotate_right_button.pack(side=tk.LEFT, padx=10)

        save_button = tk.Button(image_win, text="Speichern", command=lambda: save_rotation(canvas.rotation_angle))
        save_button.pack(side=tk.LEFT, padx=10)

        # gitter zeichnen
        draw_grid(canvas, rotated_image_pil.width, rotated_image_pil.height)

       
        canvas.image = image_tk

    else:
        messagebox.showwarning("Fehler", f"Die Datei '{image_path}' existiert nicht.")


def draw_grid(canvas, width, height):
    # vertikale linien zeichnen
    for x in range(0, width, 20):
        canvas.create_line(x, 0, x, height, fill="gray", tags="grid")

    # horizontale linien zeichnen
    for y in range(0, height, 20):
        canvas.create_line(0, y, width, y, fill="gray", tags="grid")

def rotate_image(canvas, angle):
    # aktuelle rotationswinkel abrufen und anpassen
    canvas.rotation_angle += angle

    
    rotated_image_pil = canvas.original_image_pil.copy()

    # rotiert das kopierte bild um den angegebenen Winkel
    rotated_image_pil = rotated_image_pil.rotate(canvas.rotation_angle, expand=True)

    
    rotated_image_tk = ImageTk.PhotoImage(rotated_image_pil)

   
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=rotated_image_tk)

    # gitter erneut zeichnen
    draw_grid(canvas, rotated_image_pil.width, rotated_image_pil.height)

 
    canvas.image = rotated_image_tk

def save_rotation(rotation_angle):
    print(f"Rotationswinkel: {rotation_angle} Grad")
    selected_option = dropdown_var.get()
    if selected_option and selected_option != "Bitte wählen":
        ini_file_path = os.path.join("ini", f"{selected_option}.ini")
        config = configparser.ConfigParser()
        config.read(ini_file_path)

        # Den Rotationswinkel unter dem Schlüssel "Rotation" in der INI-Datei speichern
        config.set('Settings', 'Rotation', str(rotation_angle))

        with open(ini_file_path, 'w') as configfile:
            config.write(configfile)

        print(f"Rotationswinkel {rotation_angle} Grad wurde in {ini_file_path} gespeichert.")
    else:
        messagebox.showwarning("Achtung", "Bitte wählen Sie eine INI-Datei aus.")


# button "Rotieren" erstellen
rotieren_button = tk.Button(root, text="Rotieren", command=rotieren_function)
rotieren_button.pack(pady=5)

# button "Scan bearbeiten" erstellen
edit_button = tk.Button(root, text="Scan bearbeiten", command=edit_scan)
edit_button.pack(pady=5)

# button "Scan erstellen" erstellen
scan_button = tk.Button(root, text="Scan erstellen", command=create_scan)
scan_button.pack(pady=5)

# bropdown aktualisieren
update_dropdown_options()

# button "MQTT Bearbeiten" erstellen
mqtt_edit_button = tk.Button(root, text="MQTT Bearbeiten")
mqtt_edit_button.pack(pady=10)

# gUI starten
root.mainloop()