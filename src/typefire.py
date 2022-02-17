import fire
import functools
import inspect
from typing import List, Optional, Union, Any, Callable, Sequence, Dict

from SimilarNeuron import Switch, Agreement

class TypeFire:

    agreement = Agreement()

    @classmethod
    def get_func_annotations(cls, func: Callable) -> Dict[str, Any]:
        sig = inspect.signature(func)
        return {name:param.annotation for name, param in sig.parameters.items() if param.annotation != inspect._empty}

    @classmethod
    def get_func_bind(cls, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        sig = inspect.signature(func)
        return {k:v for k,v in sig.bind(*args, **kwargs).arguments.items()}

    @classmethod
    def switch(cls, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        func_annotations = cls.get_func_annotations(func)
        func_bind = cls.get_func_bind(func, *args, **kwargs)
        for k,v in func_bind.items():
            if k in func_annotations:
                if type(v) != func_annotations[k]:
                    func_bind[k] = cls.agreement.transformation(v, func_annotations[k])
        return func_bind

    @classmethod
    def add_switch(cls, agreemap: Switch) -> Any:
        return cls.agreement.add(agreemap)

    @classmethod
    def remove_switch(cls, external: Any, internal: Any) -> Any:
        return cls.agreement.remove(external, internal)
    
    @classmethod
    def clear(cls):
        return cls.agreement.clear()

def likefire(obj):
    @functools.wraps(obj)
    def wrapper(command: str, *args, **kwargs):
        try:
            return fire.Fire(obj, command)
        except fire.core.FireExit:
            return None
    return wrapper

def typeswitch(obj):
    @functools.wraps(obj)
    def wrapper(*args, **kwargs):
        return obj(**TypeFire.switch(obj, *args, **kwargs))
    return wrapper

def typefire(func):
    return likefire(typeswitch(func))

def composed(*decs, is_reversed=False):
    def deco(f):
        if is_reversed:
            for dec in reversed(decs):
                f = dec(f)
        else:
            for dec in decs:
                f = dec(f)
        return f
    return deco
