#funktion zur berechnung des zeigers auf einer gauge. zusammenhang mit bild_gauge_finden.py

def get_gauge_value(needle_angle, min_angle, max_angle, min_value, max_value):
    # umrechnung des winkels in einen wert im angegebenen wertebereich
    value_range = max_value - min_value
    angle_range = max_angle - min_angle
    angle_per_unit = angle_range / value_range

    value = (needle_angle - min_angle) / angle_per_unit + min_value
    return value

min_angle = 130
max_angle = 290
min_value = 0
max_value = 150
needle_angle = 162

gauge_value = get_gauge_value(needle_angle, min_angle, max_angle, min_value, max_value)
print("Gauge-Wert:", gauge_value)
