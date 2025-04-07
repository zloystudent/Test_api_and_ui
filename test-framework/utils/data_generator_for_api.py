import random
import string
from typing import Dict, Any


def generate_random_string(length: int = 10) -> str:
    letters = string.ascii_letters  # both uppercase and lowercase letters
    digits = string.digits  # 0-9
    special_chars = string.punctuation  # special characters like !@#$%^&*()_+

    all_chars = letters + digits + special_chars

    random_string = [
        random.choice(letters),
        random.choice(digits),
        random.choice(special_chars),
    ]

    for _ in range(length - 3):
        random_string.append(random.choice(all_chars))

    random.shuffle(random_string)

    result = "".join(random_string)

    return result


def generate_entity_data() -> Dict[str, Any]:
    return {
        "addition": {
            "additional_info": "Дополнительные сведения",
            "additional_number": 123,
        },
        "important_numbers": [42, 87, 15],
        "title": f"Валидирующий заголовок {generate_random_string()}",
        "verified": True,
    }
