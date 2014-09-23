# ()

import re


def tokenize(s):
    return re.findall(r"[()]|\w+", s)


def read(s):
    tokens = tokenize(s)
    t = iter(tokens)
    assert next(t) == "("
    return read_tokens(t)


def read_tokens(tokens):
    l = []
    while True:
        current = next(tokens)  # try except for catching syntax errors
        if current == "(":
            l.append(read_tokens(tokens))
        elif current == ")":
            return l
        else:
            l.append(current)

def eval(ast):
