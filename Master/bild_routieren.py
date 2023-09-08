# -*- coding: utf-8 -*-

from PIL import Image, ImageTk, ImageDraw
import tkinter as tk

# datei der rotationseinstellungen
current_rotation = 0
new_rotation = 0
rotation_file = "Settings/rotation.txt"

# Flesend er rotationsdaten
def read_rotation_setting():
    try:
        with open(rotation_file, "r") as file:
            rotation = int(file.read())
            return rotation
    except FileNotFoundError:
        return 0

# schreiben in rotsationsdateo
def write_rotation_setting(rotation):
    with open(rotation_file, "w") as file:
        file.write(str(rotation))

# funktion um das bild zu routieren
def rotate_image(rotation):
    global current_rotation, new_rotation

    # berechnung der drehung
    new_rotation = current_rotation + rotation

    # rotiere das bild
    rotated_image = image.rotate(new_rotation)

    # ein gitter wird hinzugefügt
    grid_image = add_grid(rotated_image)

    # das bild wird aktualiert angezeigt
    img = ImageTk.PhotoImage(grid_image)
    canvas.itemconfig(image_item, image=img)
    canvas.image = img

    # rotations wird aktualisiert
    current_rotation = new_rotation

# funktion für gitter
def add_grid(image):
    # kopie des bilder wird erstellt
    grid_image = image.copy()

    # zeichenobjekt wird erstelle
    draw = ImageDraw.Draw(grid_image)

    # gitter größe
    grid_size = 20

    # horizontal linien in rot
    for y in range(0, grid_image.height, grid_size):
        line = ((0, y), (grid_image.width, y))
        draw.line(line, fill=(255, 0, 0))  

    # vertikale linien in rot
    for x in range(0, grid_image.width, grid_size):
        line = ((x, 0), (x, grid_image.height))
        draw.line(line, fill=(255, 0, 0))  

    return grid_image

# schlie0en der anwendung
def close_app():
    write_rotation_setting(new_rotation)
    window.destroy()

# hauptprogramm
def main():
    global image, canvas, image_item, window

    # gui fenster
    window = tk.Tk()
    window.title("Bildrotation")
    window.geometry("900x800")

    # ladet das bild
    image_path = r"3_digital.jpg"
    try:
        image = Image.open(image_path)
    except IOError:
        print("Fehler beim Lesen des Bildes.")
        return

    # camvas anzeige des bildes in 500x500
    canvas = tk.Canvas(window, width=500, height=500)
    canvas.pack()

    #bild in thinkertk
    img = ImageTk.PhotoImage(image)

    # bild wird angezigt
    image_item = canvas.create_image(200, 200, image=img)

    # Lrotationsdaten werden gelesen 
    current_rotation = read_rotation_setting()

    # bild wir mit den gelesen rotationsdaten angezeigt
    rotate_image(current_rotation)

    # button für die rotation recht und linksrum
    clockwise_button = tk.Button(window, text="Rechtsrum", command=lambda: rotate_image(1))
    clockwise_button.pack(side=tk.LEFT)

    counterclockwise_button = tk.Button(window, text="Linksrum", command=lambda: rotate_image(-1))
    counterclockwise_button.pack(side=tk.LEFT)

    # button für scjöießen und speichern der rotationsdaten
    close_button = tk.Button(window, text="Beenden", command=close_app)
    close_button.pack()
    window.protocol("WM_DELETE_WINDOW", close_app)

    window.mainloop()

if __name__ == "__main__":
    main()
