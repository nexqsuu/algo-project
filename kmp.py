def kmp_table(P: str) -> list[int]:
    """
    This function generates the KMP table for a given string.

    Args:
      s: The input string.

    Returns:
      The KMP table for the input string.
    """
    if P == '':
        return []
    M = len(P)
    # the current position we are computing in s
    # the zero-based index in W of the next character of the current candidate substring
    f = [-1] * M # failure function
    f[0] = 0
    k = 1
    while k < M:
        i = k-1
        x = f[i]

        while P[x] != P[k]:
            i = x-1
            if i < 0:
                break
            x = f[i]

        if i < 0:
            f[k] = 0
        else:
            f[k] = f[i] + 1
        k+=1
    return f

def kmp_search(search_space: str, pattern: str, max_matches: int = 1):
    # iterative version
    TABLE = kmp_table(pattern)
    M = len(pattern) 
    N = len(search_space)
    matches = []
    j = 0 # The current index in the search space.
    k = 0 # The current index in the pattern.
    while j < N:
        if pattern[k] == search_space[j]:
            j += 1
            k += 1
            if k == M:
                matches.append(j - k)
                if len(matches) == max_matches:
                    return matches
                k = 0
        else:
            if k == 0:
                j += 1
            else:
                k = TABLE[k - 1]
    return matches

def output(text: str, pattern: str, matches: list[int]):
    """Output the matches found"""
    print(f"\n{text=}")
    print(f"{pattern=}")
    print(f"Position/s: {matches}" if matches else "Pattern not found")
def main():
    """Run if main module"""
    #  single match
    text = "ABC ABCDAB ABCDABCDABD"
    pattern = "ABCDABD"
    output(text, pattern, kmp_search(text, pattern))
    print()
    # multiple matches
    text = "AAABCE ABC"
    pattern = "AAA"
    output(text, pattern, kmp_search(text, pattern, 2))

    # empty pattern
    text = "blank"
    pattern = ""
    output(text, pattern, kmp_search(text, pattern))

    # dots
    text = "test..."
    pattern = "..."
    output(text, pattern, kmp_search(text, pattern))


if __name__ == "__main__":
    main()
