import paho.mqtt.client as mqtt
import datetime

# verbindung zum mqtt broker
client = mqtt.Client()
client.connect("127.0.0.1", 1883, 60)

# aktuelles datum - fake daten zum testen
datum = "WETTER"
wert = "DONNERWETTERCCCC"

# topic festlegen
topic = "messwerte"

# nachricht
nachricht = f"Datum: {datum}, Wert: {wert}"

# an mqtt senden
client.publish(topic, nachricht)

# verbindung abbrechen
client.disconnect()