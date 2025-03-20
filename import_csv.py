import sqlite3
import csv

def import_csv_to_db(csv_file, db_file):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS burials')

    c.execute('''CREATE TABLE IF NOT EXISTS burials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        section TEXT,
        lot TEXT,
        name TEXT,
        dob TEXT,
        dod TEXT,
        stone TEXT,
        notes TEXT,
        direction TEXT
    )''')

    with open(csv_file, newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            c.execute('''INSERT INTO burials (section, lot, name, dob, dod, stone, notes, direction)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                      (row['SECTION'], row['LOT'], row['NAME'], row['DOB'], row['DOD'], row['STONE'], row['NOTES'], row['DIRECTION']))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    import_csv_to_db("burials.csv", "database.db")
