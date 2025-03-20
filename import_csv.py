import sqlite3
import csv

# Import CSV and create database
# Now verifies CSV row count and prints first few rows for debugging.
def import_csv_to_db(csv_file, db_file):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

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

    with open(csv_file, newline='', encoding='utf-8-sig') as file:  # Handle potential BOM issues
        reader = csv.DictReader(file)
        rows = list(reader)  # Convert reader to list to count rows        
        print(f"Total rows detected in CSV: {len(rows)}")
        print("First few rows for verification:")
        for i, row in enumerate(rows[:5]):
            print(f"Row {i+1}: {row}")
        
        row_count = 0
        for row in rows:
            print(f"Processing row {row_count + 1}: {row}")  # Print each row
            section = row.get('SECTION', '') or ''
            lot = row.get('Lot', '') or ''
            name = row.get('NAME', '') or ''
            dob = row.get('DOB', '') or ''
            dod = row.get('DOD', '') or ''
            stone = row.get('STONE', '') or ''
            notes = row.get('Notes', '') or ''
            direction = row.get('Direction', '') or ''

            c.execute('''INSERT INTO burials (section, lot, name, dob, dod, stone, notes, direction)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                      (section, lot, name, dob, dod, stone, notes, direction))
            conn.commit()  # Commit each row to ensure persistence
            row_count += 1

    conn.close()
    print(f"✅ Import completed successfully! {row_count} rows inserted.")

if __name__ == "__main__":
    import_csv_to_db("burials.csv", "database.db")


