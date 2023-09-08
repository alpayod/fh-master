import cv2
import numpy as np

# bild laden
image = cv2.imread('/Users/alpayodag/ONEDRIVE/Dokumente/Master/Pyhton/MasterProjekt_Server/muell/leuchten/schaltsystem_rot_an_links.png')

# rgb in hsv
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# hsv durchschnitt wird berechnet
h_avg, s_avg, v_avg = cv2.mean(hsv_image)[:3]

# aufrunden
h_avg = int(round(h_avg))
s_avg = int(round(s_avg))
v_avg = int(round(v_avg))

# werte für die überprüfung. müssen übertragem werden
print(f'Durchschnittliche HSV-Werte: Hue (H): {h_avg}, Saturation (S): {s_avg}, Value (V): {v_avg}')
