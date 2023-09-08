import cv2
import easyocr
import numpy as np

# schärfungskern definieren
kernel = np.array([[-1, -1, -1],
                   [-1, 9, -1],
                   [-1, -1, -1]])

def bild_vorverarbeiten(image_path):
    # bild laden
    image = cv2.imread(image_path)

    # originalbild anzeigen
    cv2.imshow('Originalbild', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # graustufenbild 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # zeige graustufenbild an
    cv2.imshow('Graustufen', gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # rauchunterdrücken mit gaussianblur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # zeige rauschunterdrückung an
    cv2.imshow('Rauschunterdrueckung', blurred)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # kanten schärfen
    sharpened = cv2.filter2D(blurred, -1, kernel)

    # Zzeige geschärftes bild an
    cv2.imshow('Geschaerft', sharpened)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # speichern des bildes 
    cv2.imwrite("vorverarbeitetes_bild.jpg", sharpened)

    return "vorverarbeitetes_bild.jpg"

def erkennen_zahl(image_path):
    #ocr modell auswählen
    reader = easyocr.Reader(['en'])

    # vorbereitestes bild laden 
    preprocessed_image_path = bild_vorverarbeiten(image_path)

    # erkenneung durchführen
    result = reader.readtext(preprocessed_image_path)

    # text und wahrscheinlichkeit ausgeben
    if result:
        erkannte_zahl = result[0][1]
        wahrscheinlichkeit = result[0][2]

        return erkannte_zahl, wahrscheinlichkeit
    else:
        return "Keine Zahl erkannt", 0.0

if __name__ == "__main__":
    #pfad zum bild
    bildpfad = "muell/zahlen/cropped_image3.jpg"  
    erkannte_zahl, wahrscheinlichkeit = erkennen_zahl(bildpfad)
    
    print(f"Erkannte Zahl: {erkannte_zahl}")
    print(f"Wahrscheinlichkeit: {wahrscheinlichkeit:.2f}")
