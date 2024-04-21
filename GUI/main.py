from pyscript import window, document, display
from kmp import kmp_recursive_search
from split import split_string, highlight, timer
from rk import RabinKarp
from boyer import BoyerMoore, boyer_moore
import time

textElement = document.querySelector("#text")
patternElement = document.querySelector("#pattern")
selectElement = document.querySelector("#Algorithms")
modeElement = document.querySelector("#modes")

# optimization through globalizing values
invert = patternElement.value[::-1]
spliced = []
for n in patternElement.value:
    if n == "A":
        spliced.append("T")
    elif n == "C":
        spliced.append("G")
    elif n == "T":
        spliced.append("A")
    elif n == "G":
        spliced.append("C")
    else:
        spliced.append(n)

pattern = "".join(spliced)
replace_inverted = pattern[::-1]

def start_search(event):
    outputElement = document.querySelector(".output")
    outputElement.innerHTML = ''

    timerElement = document.querySelector(".timer")
    timerElement.innerHTML = 'Time: '

    if (selectElement.value == "Knuth-Morris-Pratt"):
        start = time.perf_counter()
        result = kmp_recursive_search(textElement.value, patternElement.value, 3)
        stop = time.perf_counter()
        duration = stop - start
        timer(duration)

        parts = split_string(textElement.value, patternElement.value, result)
        print(parts)
        highlight(parts)
        if (modeElement.value == "DNA"):
            invert = patternElement.value[::-1]
            spliced = []
            for n in patternElement.value:
                if n == "A":
                    spliced.append("T")
                elif n == "C":
                    spliced.append("G")
                elif n == "T":
                    spliced.append("A")
                elif n == "G":
                    spliced.append("C")
                else:
                    spliced.append(n)

            pattern = "".join(spliced)
            replace_inverted = pattern[::-1]

            invert_result = kmp_recursive_search(textElement.value, invert, 3)
            invert_split = split_string(textElement.value, invert, invert_result)
            print(invert_split)
            highlight(invert_split)

    
            pattern_result = kmp_recursive_search(textElement.value, pattern, 3)
            pattern_split = split_string(textElement.value, pattern, pattern_result)
            print(pattern_split)
            highlight(pattern_split)


            ri_result = kmp_recursive_search(textElement.value, replace_inverted, 3)
            ri_split = split_string(textElement.value, replace_inverted, ri_result)
            print(ri_split)
            highlight(ri_split)


        
    elif (selectElement.value == "Boyer-Moore"):
        start = time.perf_counter()
        p_bm = BoyerMoore(patternElement.value)
        bm = boyer_moore(patternElement.value, p_bm, textElement.value)
        stop = time.perf_counter()
        duration = stop - start
        timer(duration)

        parts = split_string(textElement.value, patternElement.value, bm)
        highlight(parts)
        print(parts)

        if (modeElement.value == "DNA"):
            invert = patternElement.value[::-1]
            spliced = []
            for n in patternElement.value:
                if n == "A":
                    spliced.append("T")
                elif n == "C":
                    spliced.append("G")
                elif n == "T":
                    spliced.append("A")
                elif n == "G":
                    spliced.append("C")
                else:
                    spliced.append(n)

            pattern = "".join(spliced)
            replace_inverted = pattern[::-1]

            pbm_inverted = BoyerMoore(invert)
            invert_result = boyer_moore(invert, pbm_inverted, textElement.value)
            invert_split = split_string(textElement.value, invert, invert_result)
            print(invert_split)
            highlight(invert_split)

            pbm_replaced = BoyerMoore(pattern)
            pattern_result = boyer_moore(pattern, pbm_replaced, textElement.value)
            pattern_split = split_string(textElement.value, pattern, pattern_result)
            print(pattern_split)
            highlight(pattern_split)

            pbm_replacedinverted = BoyerMoore(replace_inverted)
            ri_result = boyer_moore(replace_inverted, pbm_replacedinverted, textElement.value)
            ri_split = split_string(textElement.value, replace_inverted, ri_result)
            print(ri_split)
            highlight(ri_split)



    elif (selectElement.value == "Rabin-Karp"):
        start = time.perf_counter()
        rk = RabinKarp(textElement.value, patternElement.value)
        rk.search()
        stop = time.perf_counter()
        duration = stop - start
        timer(duration)

        parts = split_string(textElement.value, patternElement.value, rk.matches)
        highlight(parts)
        print(parts)

        if (modeElement.value == "DNA"):
            invert = patternElement.value[::-1]
            spliced = []
            for n in patternElement.value:
                if n == "A":
                    spliced.append("T")
                elif n == "C":
                    spliced.append("G")
                elif n == "T":
                    spliced.append("A")
                elif n == "G":
                    spliced.append("C")
                else:
                    spliced.append(n)

            pattern = "".join(spliced)
            replace_inverted = pattern[::-1]

            invert_result = RabinKarp(textElement.value, invert)
            invert_result.search()
            invert_split = split_string(textElement.value, invert, invert_result.matches)
            print(invert_split)
            highlight(invert_split)

            pattern_result = RabinKarp(textElement.value, pattern)
            pattern_result.search()
            pattern_split = split_string(textElement.value, pattern, pattern_result.matches)
            print(pattern_split)
            highlight(pattern_split)


            ri_result = RabinKarp(textElement.value, replace_inverted)
            ri_result.search()
            ri_split = split_string(textElement.value, replace_inverted, ri_result.matches)
            print(ri_split)
            highlight(ri_split)




        

# every algo should accept:
# 1. `s` - string to be searched
# 2. `p` - the pattern
# 3. `n` - how many matches
# then return:
# a list of starting positions of the patterns