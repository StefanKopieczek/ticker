import datetime


def parse_float_range(range_str):
    """Parse a string of the form "a - b" into a pair of the form
       (float(a), float(b)"""
    split_range = range_str.split('-')
    try:
        return (float(split_range[0]), float(split_range[1]))
    except IndexError as e:
        raise ValueError(e)


def parse_int(int_str):
    """Parse a string of the form 1,234,567b into a Python integer.
       The terminal letter, if present, indicates e.g. billions."""
    int_str = int_str.replace(',', '')

    factor = __get_factor(int_str)
    if factor != 1:
        int_str = int_str[:-1]

    return int(int_str.replace(',', '')) * factor


def parse_float(float_str):
    """Parse a string of the form 305.48b into a Python float.
       The terminal letter, if present, indicates e.g. billions."""
    factor = __get_factor(float_str)
    if factor != 1:
        float_str = float_str[:-1]

    return float(float_str.replace(',', '')) * factor


def __get_factor(num_str):
    if num_str[-1] == 'b':
        return 1000000000
    elif num_str[-1] == 'm':
        return 1000000
    elif num_str[-1] == 'k':
        return 1000

    return 1


def parse_date(date_str):
    """Parse a date of the form 23-Oct-14 into a Python date object."""
    return datetime.datetime.strptime(date_str, "%d-%b-%y").date()
