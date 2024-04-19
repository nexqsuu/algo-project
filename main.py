from pyscript import window, document, display
from kmp import kmp_recursive_search
from split import split_string, highlight
from rk import RabinKarp

textElement = document.querySelector("#text")
patternElement = document.querySelector("#pattern")
selectElement = document.querySelector("#Algorithms")
# next: run the algo based on the selected option


def start_search(event):
    outputElement = document.querySelector(".output")
    outputElement.innerHTML = ''

    if (selectElement.value == "Knuth-Morris-Pratt"):
        result = kmp_recursive_search(textElement.value, patternElement.value, 3)

        parts = split_string(textElement.value, patternElement.value, result)

        highlight(parts)
        print(parts)

        
    elif (selectElement.value == "Boyer-Moore"):
        display("Boyer-Moore")

    elif (selectElement.value == "Rabin-Karp"):
        rk = RabinKarp(textElement.value, patternElement.value)
        rk.search()

        parts = split_string(textElement.value, patternElement.value, rk.matches)
        highlight(parts)
        print(parts)

# every algo should accept:
# 1. `s` - string to be searched
# 2. `p` - the pattern
# 3. `n` - how many matches
# then return:
# a list of starting positions of the patterns