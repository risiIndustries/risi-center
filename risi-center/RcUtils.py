# This file just contains whatever random functions I might need.
# Licensed Under GPL3
# By PizzaLovingNerd

import textwrap


def one_line_wrap(string, character_limit):
    if len(string) < character_limit // 2:
        return string

    s1 = textwrap.shorten(string, character_limit // 2, placeholder="")
    s2 = textwrap.shorten(string[len(s1):], character_limit // 2, placeholder="...")

    if s1[:-1] != "-":
        s2 = s2
    return '\n'.join([s1, s2])


def set_if_key(dictionary, key):
    if key in dictionary:
        var = dictionary[key]
    else:
        var = None
    return var
