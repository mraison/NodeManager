import random
import string


def generate_unique_string(length=8):
    """Generates a unique random string of given length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
