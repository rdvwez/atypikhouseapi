

def swap_quotes(string:str)-> str:
    swapped_string = ""
    in_property_name = False

    for char in string:
        if char == "'":
            if in_property_name:
                swapped_string += '"'
            else:
                swapped_string += char
        elif char == '"':
            if in_property_name:
                swapped_string += char
            else:
                swapped_string += "'"
        else:
            swapped_string += char

        if char == ":":
            in_property_name = True
        elif char in (",", "}"):
            in_property_name = False

    return swapped_string.replace("'", '"')
