from PIL import Image

# bild auswählen
image_path = input("Geben Sie den Dateipfad des Bildes ein: ")

# bild öffnen 3.jpg

image = Image.open(image_path)

# bild um die hälfte verkleinern
new_width = image.width // 2
new_height = image.height // 2
resized_image = image.resize((new_width, new_height))

# neue dateiname
output_path = image_path.replace(".jpg", "_1.jpg")

# verkleinertes bild speichern
resized_image.save(output_path)

print("Das neue Bild wurde erfolgreich gespeichert.")
