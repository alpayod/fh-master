import sqlite3

def create_database():
    # verbindung zur datenbank herstellen oder eine neue erstellen
    conn = sqlite3.connect("db_masteralpay.db")
    c = conn.cursor()

    # tabelle 'zahler' erstellen
    c.execute('''CREATE TABLE IF NOT EXISTS zahler (
                id INTEGER PRIMARY KEY,
                datum TEXT NOT NULL,
                objekt TEXT NOT NULL,
                zaehlerstand INTEGER NOT NULL
                )''')

    # tabelle 'logs' erstellen
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY,
                objekt TEXT NOT NULL,
                log TEXT NOT NULL
                )''')

    # änderungen speichern und verbindung schließen
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
