from pyscript import window, document, display
from kmp import kmp_recursive_search
textElement = document.querySelector("#text")
patternElement = document.querySelector("#pattern")
# next: run the algo based on the selected option

def start_search(event):
    print(textElement.value) # kasi element yan
    print(patternElement.value)
    display("work")
    result = kmp_recursive_search(textElement.value, patternElement.value, 3)
    # try
    for n in result:
        display(n)

# every algo should accept:
# 1. `s` - string to be searched
# 2. `p` - the pattern
# 3. `n` - how many matches
# then return:
# a list of starting positions of the patterns