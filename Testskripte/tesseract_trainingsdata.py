import pytesseract
from PIL import Image
import os
import re

# Pfad zu Trainingsdaten
os.environ['TESSDATA_PREFIX'] = '/Users/alpayodag/Downloads/tessdata'

# Bild
image_path = 'muell/zahlen/cropped_image4.jpg'

# Laden Bild
image = Image.open(image_path)

# Verwenden Tesseract mit den benutzerdefinierten Trainingsdaten
custom_data = pytesseract.image_to_string(image, config='--psm 7 --oem 3 -l digits')

# Ausgabe des erkannten Texts
print('Erkannte Zahl (benutzerdefinierte Trainingsdaten):', custom_data.strip())

# Extrahieren und ausgeben der Wahrscheinlichkeit aus der Tesseract-Ausgabe
probability_match = re.search(r'(\d+\.\d+)%', custom_data)
if probability_match:
    probability = float(probability_match.group(1))
    print('Wahrscheinlichkeit des Modells:', probability, '%')
else:
    print('Wahrscheinlichkeit des Modells nicht gefunden.')
