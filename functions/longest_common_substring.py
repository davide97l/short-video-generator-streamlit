def longest_common_substring(s1, s2):
    m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in range(1, 1 + len(s1)):
        for y in range(1, 1 + len(s2)):
            if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    return s1[x_longest - longest: x_longest]


if __name__ == '__main__':
    a = "You just need to know how people think and"
    b = "You just need to know how people think. And that's literally it besties the six books that help me go from zero to 100,000 dollar months in on the two years. It may be a secret weapon for me, but as I reminded from me to you, stop reading, just read, start reading to act. In this era of new education, we don't wait to get tested. We test ourselves. See you in the"
    common_part = longest_common_substring(a, b)
    print(common_part)  # Output: world
