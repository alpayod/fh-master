import cv2

# funktion hsv status
def überprüfe_status_bild(bildpfad):
    # laden des markierten bildes
    image = cv2.imread(bildpfad)

    # rgb in hsv
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # extraktion der hsv werte
    h_avg, s_avg, v_avg = cv2.mean(hsv_image)[:3]

    # aufrunden
    h_avg = int(round(h_avg))
    s_avg = int(round(s_avg))
    v_avg = int(round(v_avg))

    # überprüfung, ob leuchte an oder aus
    if h_avg == 29 and s_avg == 32 and v_avg == 252:
        return "eingeschaltet"
    elif h_avg == 3 and s_avg == 226 and v_avg == 153:
        return "ausgeschaltet"
    else:
        return "unbekannt"

# pfad zum bild
bild_pfad = '/Users/alpayodag/Desktop/1234.png'

# status ausgeben
status = überprüfe_status_bild(bild_pfad)
print(f"Status für das Bild: {status}")
