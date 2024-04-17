def split_string(s, pattern, list):
    parts = [] 
    start = 0
    i = 0

    while start < len(s):

        if i < len(list):
            start_index = list[i]
        else:
            parts.append(s[start:])
            break

        if start != start_index:
            parts.append(s[start:start_index])
            
        parts.append(s[start_index:start_index+len(pattern)])

        start = start_index + len(pattern)
        i += 1


    return parts
