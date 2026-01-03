import random
import string

def generate_short_code():
    # Define the set of characters: lowercase, uppercase, and digits
    characters = string.ascii_letters + string.digits
    
    # Generate and return a random 6-character alphanumeric string
    return ''.join(random.choice(characters) for _ in range(6))