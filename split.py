def split_string(s:str, pattern:str, locations:list[int]):
    parts:list[tuple[str, bool]] = [] 
    start = 0
    if len(locations) == 0:
        parts.append(s)
        return parts
    
    i = 0
    while start < len(s) and i >= len(locations):
        start_index = locations[i]
        # found or not
        part = (s[start:start_index],False)
        # add the nonmatch
        if part != '':
            parts.append(part)

        # add the match
        end_index = start_index+len(pattern)
        matched = (s[start_index:end_index], True)
        
        # appends matching substring
        parts.append(matched)
        start = end_index
        i += 1


    return parts

from pyscript import document

def highlight(parts:list[tuple[str, bool]]):
    # Get the container element
    baseElement = document.querySelector(".output")
    
    for n in parts:
        # n = ["", true or false]
        # To create an element:
        span = document.createElement('span')
        span.innerText = n[0]

        # if false walang ganto
        if n[1]:
            span.className = 'highlight'

        # Appending the element
        baseElement.append(span)