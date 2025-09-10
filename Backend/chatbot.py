import sqlite3
import google.generativeai as genai
import logging
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Configure API key
API_KEY = "AIzaSyBpGHlySBkcJ4GlpzmFe1LfuLjGfUhDZnU"
genai.configure(api_key=API_KEY)

# Configure the model
MODEL_NAME = "gemini-1.5-flash"

# Valid plant types - update this to match your app.py
VALID_PLANT_TYPES = {'rose', 'dandelion', 'sunflower', 'tulip', 'daisy'}


def init_model():
    """Initialize and return the Gemini model"""
    try:
        return genai.GenerativeModel(MODEL_NAME)
    except Exception as e:
        logger.error(f"Error initializing Gemini model: {str(e)}")
        raise


def get_chatbot_response(query: str) -> str:
    """
    Get a response to the query with plant-specific context.

    Args:
        query: The user's query (should include plant context)

    Returns:
        str: The response text
    """
    try:
        logger.debug(f"Received query: {query}")

        # Extract plant type from the query
        plant_type = None
        for valid_plant in VALID_PLANT_TYPES:
            if valid_plant.lower() in query.lower():
                plant_type = valid_plant
                break

        if not plant_type:
            return ("I can only answer questions about the identified plant. "
                    "Please make sure you've uploaded a plant image first.")

        # First check knowledge base
        predefined_answer = get_predefined_answer(query, plant_type)
        if predefined_answer:
            logger.debug("Found predefined answer")
            return predefined_answer

        # If no predefined answer, use Gemini
        logger.debug("No predefined answer found, using Gemini")
        return get_gemini_response(query, plant_type)

    except Exception as e:
        logger.error(f"Error in get_chatbot_response: {str(e)}")
        return "I apologize, but I'm having trouble generating a response. Please try again."


def get_predefined_answer(query: str, plant_type: str) -> Optional[str]:
    """Fetch predefined answer from knowledge base"""
    try:
        # Use relative path assuming plants.db is in the same directory
        conn = sqlite3.connect('plants.db')  # Modified path
        cursor = conn.cursor()

        # Improved query matching
        cursor.execute(
            """
            SELECT answer FROM knowledge_base 
            WHERE LOWER(plant_type) = LOWER(?)
            AND LOWER(?) LIKE '%' || LOWER(question) || '%'
            ORDER BY LENGTH(question) ASC
            LIMIT 1
            """,
            (plant_type, query)
        )
        result = cursor.fetchone()
        return result[0] if result else None

    except sqlite3.Error as e:
        logger.error(f"Database error: {str(e)}")
        return None
    finally:
        if 'conn' in locals():
            conn.close()


def get_gemini_response(query: str, plant_type: str) -> str:
    """
    Get a response from Gemini model with plant-specific context.

    Args:
        query: The user's query
        plant_type: The identified plant type

    Returns:
        str: The generated response
    """
    try:
        model = init_model()

        # Add specific plant context and constraints
        enhanced_query = f"""
        As a plant expert, please provide a helpful and accurate response about {plant_type} plants to this question: {query}

        Important constraints:
        1. Only provide information specifically about {plant_type} plants
        2. If the question is not specifically about {plant_type} plants, politely redirect the user to ask about {plant_type}s
        3. If you're not confident about the information specific to {plant_type} plants, acknowledge that and suggest consulting a local plant expert
        4. Keep the response focused, practical, and easy to understand
        5. Include specific care tips for {plant_type}s when relevant

        Response guidelines:
        - Keep answers concise but informative
        - Focus on practical advice
        - Use simple, clear language
        - Include specific details about {plant_type}s
        """

        response = model.generate_content(enhanced_query)

        if not response or not response.text:
            raise ValueError("Empty response from Gemini")

        cleaned_response = response.text.strip()
        logger.debug(f"Generated response: {cleaned_response}")

        # Verify the response mentions the plant type
        if plant_type.lower() not in cleaned_response.lower():
            return f"I should only provide information about {plant_type} plants. Could you please ask a specific question about {plant_type}s?"

        return cleaned_response

    except Exception as e:
        logger.error(f"Error in get_gemini_response: {str(e)}")
        return f"I apologize, but I'm having trouble generating a response. Please try asking specific questions about {plant_type} plants."


# Initialize the model at module level
try:
    model = init_model()
    logger.info("Gemini model initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Gemini model: {str(e)}")