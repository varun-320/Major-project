import sqlite3

# Database name
DB_NAME = 'plants.db'

def populate_plants_table():
    """Add new plants to the databaseh."""
    new_plants = [
        ("Marigold", "Tagetes", "Full sun, well-drained soil, moderate watering",
         "A vibrant flower known for its pest-repellent properties.", "https://example.com/marigold.jpg"),
        ("Lavender", "Lavandula", "Full sun, sandy soil, low watering",
         "A fragrant plant with soothing properties.", "https://example.com/lavender.jpg")
    ]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.executemany('''
            INSERT INTO plants (common_name, scientific_name, growth_conditions, description, image_url)
            VALUES (?, ?, ?, ?, ?)
        ''', new_plants)
        conn.commit()
        print("Plants table populated successfully!")
    except sqlite3.Error as e:
        print(f"Error populating plants table: {e}")
    finally:
        conn.close()

def populate_knowledge_base():
    """Add new Q&A pairs to the knowledge base."""
    new_qa_pairs = [
        (6, "What are the uses of Marigold?", "Marigolds repel pests and are used in decorations."),
        (6, "How often should I water Marigold?", "Water Marigolds once a week."),
        (7, "What is Lavender used for?", "Lavender is used for aromatherapy and herbal remedies."),
        (7, "Does Lavender attract pollinators?", "Yes, Lavender attracts bees and butterflies."),
        (5, "How long do daisy flowers last?", "Daisy flowers typically last for several weeks, but this can vary depending on the variety and growing conditions."),
        (5, "What are the medicinal properties of daisies?", "Daisies have been used in traditional medicine to treat a variety of ailments, including inflammation, skin conditions, and respiratory problems."),
        (5,"How do I propagate daisies?", "Daisies can be propagated by seed or by dividing established plants."),
        (4,"Are all parts of a dandelion edible?", "Yes, all parts of a dandelion are edible, including the roots, leaves, and flowers."),
        (4,"What are the health benefits of dandelion root tea?", "Dandelion root tea is believed to have liver-protective properties and can help with digestion."),
        (4,"How can I control dandelion growth in my lawn organically?", "You can control dandelion growth in your lawn by pulling them by hand, using a hoe, or applying a pre-emergent herbicide."),
        (4,"Can dandelions be used to make wine?", "Yes, dandelions can be used to make wine, although it is a less common practice."),
        (4,"What is the difference between a dandelion and a cat’s ear?", "Dandelions have smooth, hairless leaves,while cat's ears have hairy leaves."),
        (3,"What are some common rose pests and diseases?", "Common rose pests include aphids, Japanese beetles, and rose slugs.Common diseases include black spot and powdery mildew."),
        (3,"Can I grow roses in containers?", "Yes, you can grow roses in containers, but they will require more frequent watering and fertilization.")

    ]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.executemany('''
            INSERT INTO knowledge_base (plant_id, question, answer)
            VALUES (?, ?, ?)
        ''', new_qa_pairs)
        conn.commit()
        print("Knowledge base populated successfully!")
    except sqlite3.Error as e:
        print(f"Error populating knowledge base: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    populate_plants_table()
    populate_knowledge_base()
