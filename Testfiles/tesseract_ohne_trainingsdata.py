import pytesseract
from PIL import Image

# Pfad zum Tesseract-Executable 
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

# Lade das Bild
img = Image.open('/Users/alpayodag/ONEDRIVE/Dokumente/Master/Pyhton/MasterProjekt_Server/cropped_image.jpg')

# Verwende Tesseract zur Zahlen-Erkennung
erkannte_zahlen = pytesseract.image_to_string(img, config='--psm 7 outputbase digits')

# Gib die erkannten Zahlen aus
print("Erkannte Zahlen:")
print(erkannte_zahlen)
