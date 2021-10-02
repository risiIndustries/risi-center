# This file just contains whatever random functions I might need.
# Licensed Under GPL3
# By PizzaLovingNerd

import textwrap


# Wraps a string one line (used because the Gtk line wrap feature doesn't have a line limit)
def one_line_wrap(string, character_limit):
    if len(string) < character_limit // 2:
        return string

    s1 = textwrap.shorten(string, character_limit // 2, placeholder="")
    s2 = textwrap.shorten(string[len(s1):], character_limit // 2, placeholder="...")

    if s1[:-1] != "-":
        s2 = s2
    return '\n'.join([s1, s2])

# Checks to see if a dictionary contains a key
# and returns that key if it has it (or returns none).
# This is used to check if an argument exists on a function.
def set_if_key(dictionary, key):
    if key in dictionary:
        var = dictionary[key]
    else:
        var = None
    return var
