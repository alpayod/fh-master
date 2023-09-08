import pytesseract
from PIL import Image

# pfad zu tesseract 
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'

# bild laden
img = Image.open('/Users/alpayodag/ONEDRIVE/Dokumente/Master/Pyhton/MasterProjekt_Server/cropped_image.jpg')

# tesseract ocr erkennung
erkannte_zahlen = pytesseract.image_to_string(img, config='--psm 7 outputbase digits')

# zahl ausgeben
print("Erkannte Zahlen:")
print(erkannte_zahlen)
