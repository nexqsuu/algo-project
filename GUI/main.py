from pyscript import window, document, display
from kmp import kmp_recursive_search
from split import split_string
textElement = document.querySelector("#text")
patternElement = document.querySelector("#pattern")
selectElement = document.querySelector("#Algorithms")
# next: run the algo based on the selected option


def start_search(event):
    if (selectElement.value == "Knuth-Morris-Pratt"):
        list = []
        result = kmp_recursive_search(textElement.value, patternElement.value, 3)
        # try
        for n in result:
            list.append(n)
        
        focus = split_string(textElement.value, patternElement.value, list)

        print(focus)
        
    elif (selectElement.value == "Boyer-Moore"):
        display("Boyer-Moore")
    elif (selectElement.value == "Rabin-Karp"):
        display("Rabin-Karp")


# every algo should accept:
# 1. `s` - string to be searched
# 2. `p` - the pattern
# 3. `n` - how many matches
# then return:
# a list of starting positions of the patterns