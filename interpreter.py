# ()
import operator

import re


def tokenize(s):
    return re.findall(r"[()]|[^\s()]+", s)

def read(s):
    tokens = tokenize(s)
    t = iter(tokens)
    first = next(t)
    if first == "(":
        return read_tokens(t)
    else:
        for _ in t:
            raise SyntaxError()
        return first

def read_tokens(tokens):
    """Reads the tokens inside of a s-expression"""
    l = []
    while True:
        current = next(tokens)  # try except for catching syntax errors
        if current == "(":
            l.append(read_tokens(tokens))
        elif current == ")":
            return l
        else:
            l.append(current)

def scheme_sub(*args):
    if not args:
        raise TypeError("expected 1 or more arguments")
    elif len(args) == 1:
        return -args[0]
    else:
        return reduce(operator.sub, args[1:], args[0])

default_env = {
        '+': lambda *args: sum(args),
        '-': scheme_sub
        }

def define(symbol, value, env=None):
    env[symbol] = eval(value)

special_forms = {'define': define}

def eval(ast):
    if isinstance(ast, list) and ast[0] in special_forms:
        special_forms[ast[0]](*ast[1:], env=default_env)
    elif isinstance(ast, list):
        evaled = [eval(x) for x in ast]
        return evaled[0](*evaled[1:])
    elif isinstance(ast, str) and ast.isdigit():
        return int(ast)
    elif isinstance(ast, str) and ast in default_env:
        return default_env[ast]
    else:
        raise ValueError(repr(ast))

def eval_read(s):
    return eval(read(s))

def repl():
    while True:
        print eval_read(raw_input())

if __name__ == '__main__':
    repl()
