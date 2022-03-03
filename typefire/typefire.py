import fire
import functools
import inspect
from typing import List, Optional, Tuple, Union, Any, Callable, Sequence, Dict

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
    def general_parameters(cls, func: Callable, d: dict) -> Tuple[tuple, dict]:
        args = []
        kwargs = {} 
        parse_bind = {name:parse.kind for name, parse in inspect.signature(func).parameters.items()}
        for k,v in d.items():
            if k in parse_bind:
                if parse_bind[k] == inspect.Parameter.VAR_POSITIONAL:
                    args += list(v)
                elif parse_bind[k] == inspect.Parameter.VAR_KEYWORD:
                    kwargs.update(v)
                elif parse_bind[k] == inspect.Parameter.POSITIONAL_OR_KEYWORD:
                    args.append(v)
                elif parse_bind[k] == inspect.Parameter.POSITIONAL_ONLY:
                    args.append(v)
                elif parse_bind[k] == inspect.Parameter.KEYWORD_ONLY:
                    kwargs[k] = v
        return tuple(args), kwargs

    @classmethod
    def switch(cls, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        func_annotations = cls.get_func_annotations(func)
        func_bind = cls.get_func_bind(func, *args, **kwargs)
        for k,v in func_bind.items():
            if k in func_annotations:
                if type(v) != func_annotations[k]:
                    func_bind[k] = cls.agreement.transformation(v, func_annotations[k])
        return cls.general_parameters(func, func_bind)

    @classmethod
    def capture_fire(cls):
        cls.PrintResult = fire.core._PrintResult
        fire.core._PrintResult = lambda *args, **kwargs: None
        fire.core.print = lambda *args, **kwargs: None

    @classmethod
    def freed_fire(cls):
        fire.core._PrintResult = cls.core._PrintResult
        fire.core.print = print 

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
    def awrapper(command: str, *args, **kwargs):
        try:
            res = fire.core.Fire(obj, command)
        except Exception as e:
            res = None
        async def _awrapper():
            return res
        return _awrapper()

    @functools.wraps(obj)
    def wrapper(command: str, *args, **kwargs):
        try:
            return fire.Fire(obj, command)
        except fire.core.FireExit as e:
            return None
    return awrapper if inspect.iscoroutinefunction(obj) else wrapper

def typeswitch(obj):

    @functools.wraps(obj)
    async def awrapper(*args, **kwargs):
        args, kwargs = TypeFire.switch(obj, *args, **kwargs)
        return await obj(*args, **kwargs)

    @functools.wraps(obj)
    def wrapper(*args, **kwargs):
        args, kwargs = TypeFire.switch(obj, *args, **kwargs)
        return obj(*args, **kwargs)

    return awrapper if inspect.iscoroutinefunction(obj) else wrapper

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
