import cv2
import numpy as np

# funktion überprüfung ob leuchte an oder aus plus markieren auf dem bild bei mehreren leuchten
def überprüfe_hsv_und_markiere(bildpfad, hsv_wert, toleranz=0.18):
    # ild laden
    image = cv2.imread(bildpfad)

    # rgb in hsv
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # grenzwerte inkl toleranz
    lower_bound = (
        int(hsv_wert[0] * (1 - toleranz)),
        int(hsv_wert[1] * (1 - toleranz)),
        int(hsv_wert[2] * (1 - toleranz)),
    )
    upper_bound = (
        int(hsv_wert[0] * (1 + toleranz)),
        int(hsv_wert[1] * (1 + toleranz)),
        int(hsv_wert[2] * (1 + toleranz)),
    )

    # pixel finden die in der toleranz liegen
    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

    # konturen finden
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # kopie wird erstellt
    marked_image = np.copy(image)

    # gefundene werde werden mit einem grünen rechteck markiert
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(marked_image, (x, y), (x + w, y + h), (0, 255, 0), 2)  

    # bild wird angezeigt
    cv2.imshow('Markiertes Bild', marked_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # anzahl der gefunden werte
    print(f"Anzahl der gefundenen Bereiche: {len(contours)}")

# pfad zum bild
bild_pfad = '/Users/alpayodag/ONEDRIVE/Dokumente/Master/Pyhton/MasterProjekt_Server/muell/leuchten/schaltsystem.webp'

# ursprüngloche hsv werte, nur an oder aus möglich
hsv_wert = (29, 32, 252)

# gefunderer bereich anzeigen mit toleranz
überprüfe_hsv_und_markiere(bild_pfad, hsv_wert, toleranz=0.18)
