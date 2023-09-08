import io
import csv
import locale
from datetime import datetime
from google.cloud import vision

# pfad zum bild
bild_pfad = "3.jpg"
# pfad zum API-schlüssel
schluessel_pfad = "Settings/plexiform-pilot-392619-0e0d34161c54.json"

# pfad zur datei mit den kommazahleinstellungen
kommazahlen_pfad = "Settings/kommazahlen.txt"

# pfad zum ergebnis-CSV
ergebnis_csv_pfad = "Result/ergebnis.csv"

# erstellt einen Client für die google API
client = vision.ImageAnnotatorClient.from_service_account_file(schluessel_pfad)

# lade das bild
with io.open(bild_pfad, 'rb') as bild_datei:
    bild_inhalt = bild_datei.read()

bild = vision.Image(content=bild_inhalt)

def extract_numbers(text):
    return ''.join(filter(str.isdigit, text))

# erkenne die Zahl auf dem Bild
response = client.text_detection(image=bild)
erkannte_texte = response.text_annotations
erkannte_zahl = erkannte_texte[0].description
print("!!!!!Erkannte Zahl:", erkannte_zahl)
erkannte_zahl = erkannte_zahl.replace(" ", "")
#diverse testausgaben
print("!!!!!Erkannte Zahl:", erkannte_zahl)
erkannte_zahl = extract_numbers(erkannte_zahl)
print("!!!!!Erkannte Zahl, nach entfernen:", erkannte_zahl)

# extrahier den Text
if erkannte_texte:
    erkannte_zahl = erkannte_texte[0].description
    print("Erkannte Zahl:", erkannte_zahl)

    # überprüfe, ob es sich nur um Zahlen handelt
    if erkannte_zahl.isdigit():
        print("Die erkannte Zahl besteht nur aus Zahlen.")

        # lesen der Anzahl der nachkommastellen aus der Datei
        with open(kommazahlen_pfad, 'r') as kommazahlen_datei:
            anzahl_nachkommastellen = int(kommazahlen_datei.read())

        # üerprüfen ob die Anzahl der Nachkommastellen 0 ist
        if anzahl_nachkommastellen == 0:
            formatierte_zahl = erkannte_zahl
        else:
            # teilen der zahl in kommastellen
            vorkommastellen = erkannte_zahl[:-anzahl_nachkommastellen]
            nachkommastellen = erkannte_zahl[-anzahl_nachkommastellen:]

            # formatieren der zahl
            formatierte_zahl = locale.format_string("%s.%s", (vorkommastellen, nachkommastellen))

        print("Formatierte Zahl:", formatierte_zahl)

        # aktuelles datum und uhrzeit erhalten
        aktuelles_datum_uhrzeit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("Aktuelles Datum und Uhrzeit:", aktuelles_datum_uhrzeit)

        # ergebnis in  CSV-Datei
        with open(ergebnis_csv_pfad, 'a', newline='') as csv_datei:
            schreiber = csv.writer(csv_datei, delimiter=';')

            # überprüfen, ob die datei existiert
            datei_existiert = csv_datei.tell() != 0

            # überschrift schreiben, wenn die datei neu erstellt wird
            if not datei_existiert:
                schreiber.writerow(['date', 'wert'])

            schreiber.writerow([aktuelles_datum_uhrzeit, formatierte_zahl])

    else:
        print("Die erkannte Zahl enthält andere Zeichen als Zahlen.")

else:
    print("Keine Zahl erkannt.")
