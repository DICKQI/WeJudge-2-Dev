# -*- coding: utf-8 -*-
# coding:utf-8
__author__ = 'lancelrq'


def char_to_index(keyword):

    index = 0
    keyword = keyword.lower()
    charlist = [chr(x+97) for x in range(26)]
    for s in keyword:
        if s not in charlist:
            return 0
        index *= 26
        index += (ord(s) - 97) + 1
    return index

print(char_to_index("AA"))


def gen_problem_index(value):
    try:
        v = int(value)
        outstr = ""
        while v > 0:
            if v % 26 != 0:
                outstr = chr(v % 26 + 65 - 1) + outstr
            else:
                outstr = 'Z' + outstr
            if v % 26 == 0:
                v -= 1
            v //= 26

        return outstr
    except:
        return "NaN"

print(gen_problem_index(27))