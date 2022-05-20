import ast
import inspect
import ctypes
from typing import Dict, Any

# AMT 001
def defhook(astnode: ast.NodeVisitor, name: str):
    '''AMT 001 meta-decorator'''
    def wrapper(func):
        src = inspect.getsource(func)

        if f'@{name}' in src:
            srclines = src.splitlines()
            for n, line in enumerate(srclines): 
                if f'@{name}' in line:
                    break
            src = '\n'.join(srclines[n+1:])  

        if src.startswith((' ','\t')):
            src = 'if 1:\n' + src

        top = ast.parse(src, mode='exec')

        astnode.visit(top)

        temp = {}
        exec(compile(top,'','exec'), temp, temp)

        func.__code__ = temp[func.__name__].__code__
        return func
    return wrapper

class CoverVar(ast.NodeVisitor):
    '''重载函数局部变量'''
    def __init__(self, cover: dict) -> None:
        self.cover = cover

    def visit_FunctionDef(self, node):
        code = 'import ctypes\n' + '\n'.join(
            [
                f"{k} = ctypes.cast({id(v)}, ctypes.py_object).value"
                for k, v in self.cover.items()
            ]
        )

        code_ast = ast.parse(code, mode='exec')
        node.body[:0] = code_ast.body
        self.func = node

def cover_var(namespace: Dict[str, Any]):
    def wrapper(func):
        return defhook(CoverVar(namespace), cover_var.__name__)(func)
    return wrapper
