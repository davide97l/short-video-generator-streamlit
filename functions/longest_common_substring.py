def longest_common_substring(a, b):
    """
    Finds the longest common substring between two strings using dynamic programming.

    Args:
        a (str): First string.
        b (str): Second string.

    Returns:
        str: The longest common substring.
    """
    # Initialize a DP table to store the lengths of common substrings
    dp = [[0 for _ in range(len(b) + 1)] for _ in range(len(a) + 1)]

    # Fill the DP table
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Backtrack to find the actual substring
    i, j = len(a), len(b)
    longest_str = ""
    while i > 0 and j > 0:
        if dp[i][j] > 0:
            longest_str = a[i - 1] + longest_str
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i - 1][j]:
            i -= 1
        else:
            j -= 1

    return longest_str


if __name__ == '__main__':
    a = "start reading to act. In this era of new education, we don't wait to get tested. We test ourselves."
    b = "You just need to know how people think. And that's literally it besties the six books that help me go from zero to 100,000 dollar months in on the two years. It may be a secret weapon for me, but as I reminded from me to you, stop reading, just read, start reading to act. In this era of new education, we don't wait to get tested. We test ourselves. See you in the"
    common_part = longest_common_substring(a, b)
    print(common_part)  # Output: world
