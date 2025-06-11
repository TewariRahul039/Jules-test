from ..models.product import Product
from .. import db
from sqlalchemy import or_
import re

# Helper function for extracting search term (can be refined)
def extract_search_query(message: str, keywords: list) -> str:
    lower_message = message.lower()
    for keyword in keywords:
        if keyword in lower_message:
            # Extract text after the keyword
            parts = lower_message.split(keyword, 1)
            if len(parts) > 1 and parts[1].strip():
                return parts[1].strip()
    # Fallback if no keyword matched but message implies search
    if "search" in lower_message or "find" in lower_message or "look for" in lower_message:
        # Attempt to remove common non-search words if they are the only thing left
        # This is very basic and needs a proper NLP approach for robustness
        potential_query = lower_message.replace("search", "").replace("for", "").replace("find", "").replace("look", "").strip()
        if len(potential_query.split()) > 0 : # Check if there's something left
             return potential_query
    return ""


def process_user_message(message: str) -> dict:
    lower_message = message.lower().strip()

    # Intent: Farewell
    if any(farewell in lower_message for farewell in ["bye", "goodbye", "see ya", "see you later", "take care", "exit", "quit"]):
        return {'type': 'farewell', 'text': 'Goodbye! Have a great day.'}

    # Intent: Help
    if "help" == lower_message or "what can you do" == lower_message or "assist" in lower_message:
        return {'type': 'help', 'text': "You can ask me to search for products (e.g., 'search for laptops'), or say hello/goodbye. How can I assist?"}

    # Intent: Search for products
    search_trigger_keywords = ["search for ", "find ", "look for ", "show me ", "tell me about ", "search ", "browse "]
    # More specific keywords first to guide extraction
    ordered_search_keywords_for_extraction = ["search for ", "find ", "look for ", "show me ", "tell me about ", "search ", "browse "]

    is_search_intent = any(keyword in lower_message for keyword in search_trigger_keywords)

    if is_search_intent:
        query_term = extract_search_query(message, ordered_search_keywords_for_extraction)

        if query_term:
            products = Product.query.filter(
                or_(
                    Product.name.ilike(f'%{query_term}%'),
                    Product.description.ilike(f'%{query_term}%'),
                    Product.category.ilike(f'%{query_term}%')
                )
            ).limit(5).all()

            if products:
                return {
                    'type': 'product_list',
                    'products': [p.to_dict() for p in products],
                    'text': f"Here are some products matching '{query_term}':"
                }
            else:
                return {
                    'type': 'no_results',
                    'text': f"Sorry, I couldn't find any products matching '{query_term}'."
                }
        else: # Search intent words used, but no clear term followed.
            return {'type': 'clarification', 'text': "What would you like to search for specifically?"}

    # Intent: Greeting (check after more specific intents like search)
    if any(greeting in lower_message for greeting in ["hello", "hi", "hey", "greetings", "what's up", "good morning", "good afternoon"]):
        # Make greeting check more specific to avoid triggering on partial matches within other sentences
        # For example, check if the message *starts* with a greeting or is *only* a greeting.
        greeting_starters = ["hello", "hi", "hey", "greetings"]
        if any(lower_message.startswith(g) for g in greeting_starters) or lower_message in greeting_starters:
            return {'type': 'greeting', 'text': 'Hello! How can I help you find a product today?'}

    # Default/Fallback
    return {'type': 'fallback', 'text': "Sorry, I didn't understand that. You can ask me to 'search for [product]' or ask for 'help'."}
