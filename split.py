def split_string(s:str, pattern:str, locations:list[int]):
    parts:list[tuple[str, bool]] = [] 
    start = 0
    i = 0
    print(pattern)
    
    if len(locations) == 0:
        tupled = (s, False)
        parts.append(tupled)
        return parts
    
    while start < len(s) and  i < len(locations):
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

    # if the substring doesn't end at the end of the string
    if locations[len(locations) - 1] < (len(s) - 1):
        remainder = (s[start:], False)
        # if it does end on the string we disregard
        if remainder[0] != '':
          parts.append(remainder)

    return parts

from pyscript import document

def highlight(parts:list[tuple[str, bool]]):
    # Get the container element
    baseElement = document.querySelector(".output")
    br = document.createElement('br')
    baseElement.append(br)
    
    for n in parts:
        # n = [str, bool]
        # To create an element:
        span = document.createElement('span')
        span.innerText = n[0]

        # if false walang ganto
        if n[1] != False:
            span.className = 'highlight'

        # Appending the element
        baseElement.append(span)

    baseElement.append(br)

def timer(time):
    baseElement = document.querySelector(".timer")

    span = document.createElement('span')
    span.innerText = str(time) + " s"
    baseElement.append(span)
