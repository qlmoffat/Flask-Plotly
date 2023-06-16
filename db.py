import sqlite3
import json

# Create a new SQLite database and connect to it
conn = sqlite3.connect('db.db')

cursor = conn.cursor()

# Create a table named 'countries' with the necessary columns
conn.execute('''
    CREATE TABLE IF NOT EXISTS countries (
        name TEXT,
        alpha_2 TEXT,
        alpha_3 TEXT,
        country_code TEXT,
        iso_3166_2 TEXT,
        region TEXT,
        sub_region TEXT,
        intermediate_region TEXT,
        region_code TEXT,
        sub_region_code TEXT,
        intermediate_region_code TEXT
    )
''')

# Read the JSON data from the file
with open('all.json') as file:
    json_data = file.read()

# Convert the JSON data to a Python list of dictionaries
data = json.loads(json_data)

# Insert the data into the 'countries' table
for item in data:
    values = [
        item['name'],
        item['alpha-2'],
        item['alpha-3'],
        item['country-code'],
        item['iso_3166-2'],
        item['region'],
        item['sub-region'],
        item['intermediate-region'],
        item['region-code'],
        item['sub-region-code'],
        item['intermediate-region-code']
    ]
    conn.execute('INSERT INTO countries VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', values)

# Commit the changes to the database
conn.commit()

# Close the connection
conn.close()
