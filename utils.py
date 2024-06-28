import re

def number_to_string(number):
    """
    Converts a given number into a string formatted with commas according to the Indian numbering system.
    
    Parameters:
    - number: The number to be formatted (int or float)
    
    Returns:
    A string with commas separating lakhs and crores.
    """
    s = str(int(number))
    if "." in s:
        integer_part, decimal_part = s.split(".")
    else:
        integer_part, decimal_part = s, ""

    # Reverse the integer part to process from the right (units side)
    integer_part_reversed = integer_part

    # Process for Indian numbering system
    # First three digits for thousands, then every two digits
    if len(integer_part_reversed) > 3:
        integer_part_reversed = integer_part_reversed[::-1]
        parts = [integer_part_reversed[:3]] + [integer_part_reversed[i:i+2] for i in range(3, len(integer_part_reversed), 2)]
        formatted_integer_part = ','.join(part for part in parts[::])
    else:
        formatted_integer_part = integer_part

    # Combine the integer and decimal parts
    if decimal_part:
        return (formatted_integer_part + "." + decimal_part)
    else:
        return formatted_integer_part
    
def convert_to_number_list(string_list):
    numbers = []
    for string in string_list:
        numbers.append(int(re.search(r'-?\d+$', string.replace(' ', '').replace(',', '')).group()))
    return numbers