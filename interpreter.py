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

default_scope = {
        '+': lambda *args: sum(args),
        '-': scheme_sub
        }

def define(symbol, value, env=None):
    env[-1][symbol] = eval(value, env)

def lambda_(params, exp, env=None):
    if not isinstance(params, list):
        raise SyntaxError('lambda got bad params')
    if not all(valid_symbol(x) for x in params):
        raise SyntaxError('lambda got bad params: %r', params)
    def the_function(*args):
        outer_scopes = env
        if len(args) != len(params):
            raise TypeError('Bad arity of scheme function')
        new_scope = {p: a for p, a in zip(params, args)}
        return eval(exp, env=outer_scopes + (new_scope,))
    return the_function


def valid_symbol(s):
    return isinstance(s, str) and not (s.isdigit() or s in ['#t', '#f'])

special_forms = {'define': define,
                 'lambda': lambda_}

def eval(ast, env=(default_scope,)):
    if (isinstance(ast, list) and isinstance(ast[0], str) and
            ast[0] in special_forms):
        return special_forms[ast[0]](*ast[1:], env=env)
    elif isinstance(ast, list):
        evaled = [eval(x, env=env) for x in ast]
        return evaled[0](*evaled[1:])
    elif isinstance(ast, str) and ast.isdigit():
        return int(ast)
    elif isinstance(ast, str):
        for scope in reversed(env):
            if ast in scope:
                return scope[ast]
        else:
            raise ValueError(repr(ast))
    else:
        raise ValueError(repr(ast))

def eval_read(s):
    return eval(read(s))

def repl():
    while True:
        print eval_read(raw_input())

if __name__ == '__main__':
    repl()
