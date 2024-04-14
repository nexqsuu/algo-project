from pyscript import window, document
from kmp import kmp_recursive_search

text = document.querySelector("#text")
pattern = document.querySelector("#pattern")
rec = kmp_recursive_search(text, pattern, 3)

print(text)
print(pattern)
print(f"Position/s: {rec}" if rec else "Pattern not found")


# every algo should accept:
# 1. `s` - string to be searched
# 2. `p` - the pattern
# 3. `n` - how many matches
# then return:
# a list of starting positions of the patterns

# import mo functions from kmp