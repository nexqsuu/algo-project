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
        
def kmp_recursive_search(search_space: str, pattern: str, max_matches: int = 1):
    """Knuth-MorrisPratt algorithm using recursion"""
    TABLE = kmp_table(pattern)  ## todo recursive ver of this
    M = len(pattern)
    N = len(search_space)
    def inner(j: int, k: int, matches: list[int]):
        """Recursive function to search for the pattern in the search space.
        Args:
            j: The current index in the search space.
            k: The current index in the pattern.
            M: The length of the pattern.
            N: The length of the search space.
            matches: The list of matches found.
        """
        if k == M:  # pattern found
            # append the last match to the list
            # `j-k` is the starting index of the pattern
            if len(matches) == max_matches - 1:
                # early return if max matches is reached
                return matches + [j - k] 
            return inner(j, TABLE[k-1], matches + [j - k])
        elif j == N:  # pattern does not exist
            return matches
        elif pattern[k] == search_space[j]:  # characters match
            return inner(j + 1, k + 1, matches)
        # resets the pattern
        elif k == 0:
            return inner(j + 1, max(TABLE[k], 0), matches)
        # check next
        return inner(j, TABLE[k-1], matches) 
    return inner(0, 0, [])

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
    output(text, pattern, kmp_recursive_search(text, pattern))
    print()
    # multiple matches
    text = "AAABCE ABC"
    pattern = "AAA"
    output(text, pattern, kmp_recursive_search(text, pattern, 2))

    # empty pattern
    text = "blank"
    pattern = ""
    output(text, pattern, kmp_recursive_search(text, pattern))

    # dots
    text = "test..."
    pattern = "..."
    output(text, pattern, kmp_recursive_search(text, pattern))


if __name__ == "__main__":
    main()
