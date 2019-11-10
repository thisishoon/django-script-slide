#! /usr/bin/python
# -*- coding: utf-8 -*-


def compose_char(char):
    return NotImplementedError


def compose(string):
    return NotImplementedError


def decompose_char(char):
    return NotImplementedError


def decompose(string, aslist=False):
    l = (decompose_char(c) for c in string)

    if aslist:
        return list(l)
    else:
        flattened = filter(' ', sum(l, []))
        return ''.join(flattened)


def to_unicode():
    """
    TODO
    NOTE
    FIXME
    """

    return NotImplementedError
