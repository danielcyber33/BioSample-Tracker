import sqlite3

connection = sqlite3.connect("biosamples.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM samples")

samples = cursor.fetchall()

connection.close()

print("=== AMOSTRAS CADASTRADAS ===\n")

for sample in samples:
    print(sample)