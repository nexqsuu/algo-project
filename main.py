from pyscript import window, document, display
from kmp import kmp_search
from split import split_string, highlight, timer
from rk import RabinKarp
from boyer import BoyerMoore, boyer_moore
import time

textElement = document.querySelector("#text")
patternElement = document.querySelector("#pattern")
selectElement = document.querySelector("#Algorithms")
modeElement = document.querySelector("#modes")
matchElement = document.querySelector("#n")



def start_search(event):
    outputElement = document.querySelector(".output")
    outputElement.innerHTML = ''

    timerElement = document.querySelector(".timer")
    timerElement.innerHTML = 'Time: '
    
    if isinstance(matchElement.value, str):
        matchElement.innerHTML = 1
        print(matchElement.value)
    elif matchElement.value == 0:
        matchElement.innerHTML = 1


    if (selectElement.value == "Knuth-Morris-Pratt"):
        start = time.perf_counter()
        result = kmp_search(textElement.value, patternElement.value, int(matchElement.value))
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

            replaced = "".join(spliced)
            replace_inverted = replaced[::-1]

            invert_result = kmp_search(textElement.value, invert, int(matchElement.value))
            invert_split = split_string(textElement.value, invert, invert_result)
            print(invert_split)
            highlight(invert_split)

    
            replaced_result = kmp_search(textElement.value, replaced, int(matchElement.value))
            replaced_split = split_string(textElement.value, replaced, replaced_result)
            print(replaced_split)
            highlight(replaced_split)


            ri_result = kmp_search(textElement.value, replace_inverted, int(matchElement.value))
            ri_split = split_string(textElement.value, replace_inverted, ri_result)
            print(ri_split)
            highlight(ri_split)


        
    elif (selectElement.value == "Boyer-Moore"):
        if modeElement.value == "Standard":
            start = time.perf_counter()
        bm = boyer_moore(textElement.value, patternElement.value,  int(matchElement.value))
        parts = split_string(textElement.value, patternElement.value, bm)
        highlight(parts)
        if modeElement.value == "Standard":
            stop = time.perf_counter()
            duration = stop - start
            timer(duration)
        if modeElement.value == "DNA":
            alphabet = 'ACTG'
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

            replaced = "".join(spliced)
            replace_inverted = replaced[::-1]

            start = time.perf_counter()
            invert_result = boyer_moore(textElement.value, invert,  int(matchElement.value),alphabet)
            invert_split = split_string(textElement.value, invert, invert_result)
            print(invert_split)
            highlight(invert_split)
            stop = time.perf_counter()
            duration = stop - start
            timer(duration)

            replaced_result = boyer_moore( textElement.value, replaced, int(matchElement.value), alphabet)
            replaced_split = split_string(textElement.value, replaced, replaced_result)
            print(replaced_split)
            highlight(replaced_split)

            ri_result = boyer_moore(textElement.value, replace_inverted, int(matchElement.value), alphabet)
            ri_split = split_string(textElement.value, replace_inverted, ri_result)
            print(ri_split)
            highlight(ri_split)


    elif (selectElement.value == "Rabin-Karp"):
        start = time.perf_counter()
        rk = RabinKarp(textElement.value, patternElement.value, int(matchElement.value))
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

            replaced = "".join(spliced)
            replace_inverted = replaced[::-1]

            invert_result = RabinKarp(textElement.value, invert, int(matchElement.value))
            invert_result.search()
            invert_split = split_string(textElement.value, invert, invert_result.matches)
            print(invert_split)
            highlight(invert_split)

            replaced_result = RabinKarp(textElement.value, replaced, int(matchElement.value))
            replaced_split = split_string(textElement.value, replaced, replaced_result.matches)
            print(replaced_split)
            highlight(replaced_split)

            ri_result = RabinKarp(textElement.value, replace_inverted, int(matchElement.value))
            ri_result.search()
            ri_split = split_string(textElement.value, replace_inverted, ri_result.matches)
            print(ri_split)
            highlight(ri_split)

