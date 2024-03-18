def text_remove_punctuation(text):
    """
    This function removes all punctuation from a text string.

    Args:
        text: The text string to remove punctuation from.

    Returns:
        A new string with all punctuation removed.
    """
    # Define punctuation characters
    punctuations = "!\"#$%&()*+,./:;<=>?@[]\\^_`{|}~"
    # Use translate method with a dictionary to remove punctuation
    no_punct_text = text.translate(str.maketrans('', '', punctuations))
    return no_punct_text
