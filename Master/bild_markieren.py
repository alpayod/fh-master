import cv2
import numpy as np

# pfad zum bild und zur rotationsdatei
image_path = '/Users/alpayodag/ONEDRIVE/Dokumente/Master/Pyhton/MasterProjekt_Server/links.png'
rotation_file_path = 'Master/Pyhton/MasterProjekt_Server/Settings/rotation.txt'
coordinates_file_path = 'Master/Pyhton/MasterProjekt_Server/Settings/coordinates.txt'

# bild laden
image = cv2.imread(image_path)

# rotation aus der datei lesen
rotation = 0
try:
    with open(rotation_file_path, 'r') as f:
        rotation = int(f.read())
except FileNotFoundError:
    print(f'Rotationsdatei {rotation_file_path} nicht gefunden. Das Bild wird ohne Rotation geöffnet.')

# dild rotieren
rows, cols = image.shape[:2]
M = cv2.getRotationMatrix2D((cols / 2, rows / 2), rotation, 1)
image = cv2.warpAffine(image, M, (cols, rows))

# funktion zum rechteckzeichnen
def draw_rectangle(event, x, y, flags, param):
    global drawing, top_left_pt, bottom_right_pt, image

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        top_left_pt = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        bottom_right_pt = (x, y)

        # rechteck zeichnen
        #image = cv2.imread(image_path)  #test
        cv2.rectangle(image, top_left_pt, bottom_right_pt, (0, 255, 0), 2)
        cv2.imshow('Image', image)

# fenster für das bild anzeigen
cv2.namedWindow('Image')
cv2.setMouseCallback('Image', draw_rectangle)

drawing = False
top_left_pt, bottom_right_pt = (-1, -1), (-1, -1)

while True:
    cv2.imshow('Image', image)

    # abbruchbedingung mit Taste q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

# bild mit rechteck speichern
output_path = '3_with_rectangle.jpg'
cv2.imwrite(output_path, image)
print(f'Bild mit Rechteck wurde unter {output_path} gespeichert.')

# bereich ausschneiden und speichern
if top_left_pt != (-1, -1) and bottom_right_pt != (-1, -1):
    cropped_image = image[top_left_pt[1]:bottom_right_pt[1], top_left_pt[0]:bottom_right_pt[0]]
    cropped_output_path = 'cropped_image.jpg'
    cv2.imwrite(cropped_output_path, cropped_image)
    print(f'Ausgeschnittener Bereich wurde unter {cropped_output_path} gespeichert.')

    # koordinaten der markierung speichern
    with open(coordinates_file_path, 'w') as f:
        f.write(f'Top Left: {top_left_pt}\n')
        f.write(f'Bottom Right: {bottom_right_pt}\n')
        print(f'Koordinaten der Markierung wurden unter {coordinates_file_path} gespeichert.')
