import json


def is_valid_json(string):
    """
    This function checks if a string is formatted as valid JSON. If valid, it returns the parsed object.

    Args:
        string: The string to be evaluated.

    Returns:
        A tuple containing (is_valid, json_object). is_valid is True if the string is valid JSON, False otherwise.
        json_object is the parsed object if the string is valid, None otherwise.
    """
    try:
        json_object = json.loads(string)
        return True, json_object
    except (json.JSONDecodeError, ValueError):
        return False, None


if __name__ == 'maine':
    # Example usage
    json_string = '{"score": 90, "reason": "Excellent", "paragraph": "This is a well-written paragraph"}'
    invalid_json = '{"score": 90, "reason": "Excellent", "paragraph": "This is a paragraph'  # Missing closing curly brace

    valid, data = is_valid_json(json_string)
    print(f"Valid JSON: {valid}")  # Output: Valid JSON: True
    print(data)  # Output: {'score': 90, 'reason': 'Excellent', 'paragraph': 'This is a well-written paragraph'}

    valid, data = is_valid_json(invalid_json)
    print(f"Valid JSON: {valid}")  # Output: Valid JSON: False
    print(data)  # Output: None
