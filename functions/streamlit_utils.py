def text_add_color(text:str, substring:str, color: str):
    """
    Modifies the substring a inside string b such that a becomes ':color[a]'.

    Args:
        text: The string containing the substring to modify.
        substring: The substring to modify.

    Returns:
        The modified string text.
    """
    start_index = text.find(substring)
    if start_index != -1:
        end_index = start_index + len(substring)
        return text[:start_index] + f':{color}[' + substring + ']' + text[end_index:]
    else:
        return text

