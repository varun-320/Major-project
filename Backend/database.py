

import sqlite3

def get_plant_info(plant_name):
    try:
        # Establish connection to the database
        conn = sqlite3.connect('plants.db')
        cursor = conn.cursor()

        plant_name = plant_name.capitalize()

        try:
            # Execute the query to fetch plant data
            cursor.execute("SELECT * FROM plants WHERE common_name = ?", (plant_name,))
            plant = cursor.fetchone()
        except sqlite3.Error as query_error:
            raise Exception(f"Error executing the query: {query_error}")
        finally:
            # Ensure the connection is closed after operation
            conn.close()

        # Check if a plant record was found
        if plant:
            return {
                'common_name': plant[1],
                'scientific_name': plant[2],
                'growth_conditions': plant[3],
                'description': plant[4],
                'image_url': plant[5]
            }
        else:
            raise ValueError(f"No plant found with the common name: {plant_name}")

    except sqlite3.Error as db_error:
        # Handle errors related to database connection
        print(f"Database connection error: {db_error}")
        return None

    except ValueError as no_record_error:
        # Handle case when no record is found
        print(f"Value Error: {no_record_error}")
        return None

    except Exception as general_error:
        # Handle any other exceptions
        print(f"An unexpected error occurred: {general_error}")
        return None
