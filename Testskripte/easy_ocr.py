import easyocr
import PIL.Image

def ocr_image(image_path):
    # bild ladem
    image = PIL.Image.open(image_path)

    # ocr modell auswählen
    reader = easyocr.Reader(['en'])

    # erkenneung durchführen
    results = reader.readtext(image)

    # erkannten text ausgeben
    for result in results:
        print(f"Text: {result[1]}, Koordinaten: {result[0]}")

if __name__ == "__main__":
    # pfad zum bild
    image_path = "/Users/alpayodag/ONEDRIVE/Dokumente/Master/Pyhton/MasterProjekt_Server/cropped_image.jpg"
    ocr_image(image_path)

