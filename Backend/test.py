import sqlite3

conn = sqlite3.connect('plants.db')
cursor = conn.cursor()

plant_name = "Daisy"

cursor.execute("SELECT * FROM plants WHERE common_name = ?", (plant_name,))
plant = cursor.fetchone()

print(plant)