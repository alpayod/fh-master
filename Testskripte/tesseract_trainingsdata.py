import pytesseract
from PIL import Image
import os
import re

# pfad zu trainingsdaten
os.environ['TESSDATA_PREFIX'] = '/Users/alpayodag/Downloads/tessdata'

# bildpfad
image_path = 'muell/zahlen/cropped_image4.jpg'

# bild laden
image = Image.open(image_path)

# tesseract mit trainingdaten starten
custom_data = pytesseract.image_to_string(image, config='--psm 7 --oem 3 -l digits')

# erkannten text ausgeben
print('Erkannte Zahl (benutzerdefinierte Trainingsdaten):', custom_data.strip())

# wahrscheinlichkeit ausgeben
probability_match = re.search(r'(\d+\.\d+)%', custom_data)
if probability_match:
    probability = float(probability_match.group(1))
    print('Wahrscheinlichkeit des Modells:', probability, '%')
else:
    print('Wahrscheinlichkeit des Modells nicht gefunden.')
