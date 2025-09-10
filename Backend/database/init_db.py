import sqlite3

# Database name
DB_NAME = 'plants.db'

# Initialize database connection
def initialize_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create `plants` table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plants (
            plant_id INTEGER PRIMARY KEY AUTOINCREMENT,
            common_name TEXT NOT NULL,
            scientific_name TEXT NOT NULL,
            growth_conditions TEXT NOT NULL,
            description TEXT NOT NULL,
            image_url TEXT
        )
    ''')

    # Create `knowledge_base` table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plant_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            FOREIGN KEY (plant_id) REFERENCES plants (plant_id)
        )
    ''')

    # Create `chat_history` table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            role TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')

    # Insert initial data into `plants` table
    initial_plants = [
        ("Tulip", "Tulipa", "Full sun, well-drained soil, moderate watering",
         "A spring-blooming perennial flower.", "https://example.com/tulip.jpg"),
        ("Sunflower", "Helianthus annuus", "Full sun, fertile soil, regular watering",
         "A large, bright flower popular for seeds and beauty.", "https://example.com/sunflower.jpg"),
        ("Rose", "Rosa", "Partial to full sun, fertile soil, regular pruning",
         "A fragrant, beautiful flower with many varieties.", "https://example.com/rose.jpg"),
        ("Dandelion", "Taraxacum", "Full sun, any soil, low maintenance",
         "A hardy plant with medicinal properties.", "https://example.com/dandelion.jpg"),
        ("Daisy", "Bellis perennis", "Full sun, moist soil, regular watering",
         "A cheerful flower with white petals and a yellow center.", "https://example.com/daisy.jpg")
    ]
    cursor.executemany('''
        INSERT INTO plants (common_name, scientific_name, growth_conditions, description, image_url) 
        VALUES (?, ?, ?, ?, ?)
    ''', initial_plants)

    # Insert initial data into `knowledge_base` table
    initial_knowledge_base = [
        (1, "What is the ideal soil for Tulips?", "Well-drained soil is ideal for Tulips."),
        (2, "How often should Sunflowers be watered?", "Sunflowers need regular watering, especially during dry periods."),
        (3, "How do I prune Roses?", "Prune roses in early spring, removing dead or weak stems."),
        (4, "What are the benefits of Dandelions?", "Dandelions have medicinal properties and can be used in teas and salads."),
        (5, "Do Daisies require a lot of maintenance?", "Daisies are low-maintenance and thrive in most conditions."),
        (5, "What are some common types of daisies?", "Common types of daisies include Shasta daisies, English daisies, and Gerbera daisies."),
        (5, "Can daisies be grown indoors?", "While daisies can be grown indoors, they prefer outdoor conditions and may not thrive indoors for extended periods.")

    ]
    cursor.executemany('''
        INSERT INTO knowledge_base (plant_id, question, answer) 
        VALUES (?, ?, ?)
    ''', initial_knowledge_base)

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

# Run the initialization
if __name__ == "__main__":
    initialize_database()
