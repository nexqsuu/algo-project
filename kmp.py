def kmp_table(s: str) -> list[int]:
    """
    This function generates the KMP table for a given string.

    Args:
      s: The input string.

    Returns:
      The KMP table for the input string.
    """
    M = len(s)
    # create a table of size m + 1
    table = [-1] * (M + 1)  # reserve a list w/ m + 1 size
    i = 1  # the current position we are computing in s
    j = 0  # the zero-based index in W of the next character of the current candidate substring
    while i < M:
        if s[i] == s[j]:
            table[i] = table[j]
        else:
            table[i] = j
            while j >= 0 and s[i] != s[j]:
                j = table[j]
        i += 1
        j += 1
    table[i] = j
    return table

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
            return inner(j, TABLE[k], matches + [j - k])
        elif j == N:  # pattern does not exist
            return matches
        elif pattern[k] == search_space[j]:  # characters match
            return inner(j + 1, k + 1, matches)
        # resets the pattern
        elif k < 0:
            return inner(j + 1, max(TABLE[k], 0), matches)
        return inner(j, TABLE[k], matches)  # check next
    return inner(0, 0, [])

# def main():
#     """Run if main module"""
#     #  single match
#     text = "ABC ABCDAB ABCDABCDABD"
#     pattern = "ABCDABD"
#     rec = kmp_recursive_search(text, pattern)
#     print(f"{text=}")
#     print(f"{pattern=}")
#     print(f"Position/s: {rec}" if rec else "Pattern not found")

#     print()
#     # multiple matches
#     text = "ABCE ABC"
#     pattern = "ABC"
#     rec = kmp_recursive_search(text, pattern, 3)
#     print(f"{text=}")
#     print(f"{pattern=}")
#     print(f"Position/s: {rec}" if rec else "Pattern not found")

# if __name__ == "__main__":
#     main()
