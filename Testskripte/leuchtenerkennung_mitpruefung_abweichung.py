import cv2

# funktion überprüfung ob leuchte an oder aus 
def überprüfe_status_bild(bildpfad, toleranz=0.1):
    # hsv werte auch leucherkennung.py
    eingeschaltet_hsv = (31, 146, 210)
    ausgeschaltet_hsv = (19, 145, 74)

    # bild laden
    image = cv2.imread(bildpfad)

    # rgb in hsv
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # extraktion der hsv werte
    h_avg, s_avg, v_avg = cv2.mean(hsv_image)[:3]

    # aufrunden
    h_avg = int(h_avg)
    s_avg = int(s_avg)
    v_avg = int(v_avg)

    print (h_avg)
    print (s_avg)
    print (v_avg)

    # mit abwiechung überprüfung
    def abweichung_prozent(a, b):
        return abs(a - b) / b

    h_abweichung = abweichung_prozent(h_avg, eingeschaltet_hsv[0])
    s_abweichung = abweichung_prozent(s_avg, eingeschaltet_hsv[1])
    v_abweichung = abweichung_prozent(v_avg, eingeschaltet_hsv[2])
    print (h_abweichung)
    print (s_abweichung)
    print (v_abweichung)

    if (
        h_abweichung <= toleranz
        and s_abweichung <= toleranz
        and v_abweichung <= toleranz
    ):
        return f"{bildpfad}: eingeschaltet (H: {h_avg}, S: {s_avg}, V: {v_avg})"
    else:
        return f"{bildpfad}: ausgeschaltet (H: {h_avg}, S: {s_avg}, V: {v_avg})"

# pfad zum bild
#bild_pfad = '/Users/alpayodag/ONEDRIVE/Dokumente/Master/Pyhto#n/MasterProjekt_Server/muell/leuchten/schaltsystem_rot_aus.png'
#bild_pfad = '/Users/alpayodag/ONEDRIVE/Dokumente/Master/Pyhton/MasterProjekt_Server/muell/leuchten/schaltsystem_rot_an_links.png'
#bild_pfad = '/Users/alpayodag/ONEDRIVE/Dokumente/Master/Pyhton/MasterProjekt_Server/muell/leuchten/schaltsystem_rot_an_rechts.png'
bild_pfad = '/Users/alpayodag/ONEDRIVE/Dokumente/Master/Pyhton/MasterProjekt_Server/muell/leuchten/an.png'
#bild_pfad = '/Users/alpayodag/ONEDRIVE/Dokumente/Master/Pyhton/MasterProjekt_Server/muell/leuchten/aus.png'

# berprüfen mit der toleranz
status = überprüfe_status_bild(bild_pfad, toleranz=0.1)
print(f"Status für das Bild: {status}")
