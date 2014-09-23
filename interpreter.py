# ()
import operator
import re
import traceback

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

def let(bindings, expression, env=None):
    local_scope = {var: eval(val, env) for [var, val] in bindings}
    return eval(expression, env + (local_scope,))


def valid_symbol(s):
    return isinstance(s, str) and not (s.isdigit() or s in ['#t', '#f'])

special_forms = {'define': define,
                 'lambda': lambda_,
                 'let'   : let }

def eval(ast, env):
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
            raise NameError(repr(ast))
    else:
        raise ValueError(repr(ast))

def define_code(symbol, value):
    return "locals().__setitem__('%s', %s)" % (symbol, code_gen(value))

def lambda_code(params, exp):
    if not isinstance(params, list):
        raise SyntaxError('lambda got bad params')
    if not all(valid_symbol(x) for x in params):
        raise SyntaxError('lambda got bad params: %r', params)
    return "(lambda %s : %s" % (", ".join(params), code_gen(exp)) + ")"

def let_code(bindings, expression):
    local_scope = {var: code_gen(val) for [var, val] in bindings}
    return "(lambda " + ",".join(local_scope.keys()) + " : " + code_gen(expression) + ")(" + ",".join(local_scope.values()) + ")"

special_forms_code_gen = {'define': define_code,
                          'lambda': lambda_code,
                          'let'   : let_code }

lookup_table = {'+' : "(lambda *args : sum(args))",
                '-' : "__import__('operator').sub"}


def code_gen(ast):
    if (isinstance(ast, list) and isinstance(ast[0], str) and
            ast[0] in special_forms_code_gen):
        return special_forms_code_gen[ast[0]](*ast[1:])
    elif isinstance(ast, list):
        code_parts = [code_gen(x) for x in ast]
        return code_parts[0] + "(" + ",".join(code_parts[1:]) + ")"
    elif isinstance(ast, str) and ast.isdigit():
        return ast
    elif isinstance(ast, str):
        return lookup_table.get(ast, ast)
    else:
        raise SyntaxError(repr(ast))

def eval_one(s):
    return eval_read(s, (default_scope.copy(),))

def eval_several(s_list):
    env = (default_scope.copy(),)
    for s in s_list:
        evaled = eval(s, env)
    return evaled

def eval_read(s, env):
    return eval(read(s), env)

def repl():
    initial_scope = (default_scope.copy(),)
    while True:
        print eval_read(raw_input(), initial_scope)

def python_code_repl():
    while True:
        py_code = code_gen(read(raw_input()))
        print ">> " + py_code
        try:
            print __builtins__.eval(py_code)
        except:
            traceback.print_exc()

if __name__ == '__main__':
    # repl()
    python_code_repl()
