# aufgerufenes_skript.py

import sys

if len(sys.argv) > 1:
    auswahl = sys.argv[1]
    print("Auswahl:", auswahl)
else:
    print("Keine Auswahl übergeben.")