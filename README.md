# TypeFire

通过装饰器零入侵性的，对 `fire-python` 的类型约束进行拓展，此外其还适用于任何函数对象进行基于注解的类型转换

## Fire

```python
from pathlib import Path
import fire


def test_fire(path: Path):
    print(type(path))
    print(path)


if __name__ == "__main__":
    fire.Fire(test_fire)

'''
python test_fire.py "/some_path_string"

<class 'str'>
/some_path_string
'''
```

ps: [fire #260](https://github.com/google/python-fire/issues/260#issue-620735435)

## TypeFire

```python
from src import Switch, TypeFire, typefire, typeswitch
import fire
import pathlib

TypeFire.add_switch(Switch(str, pathlib.Path, lambda p: pathlib.Path(p)))

@typeswitch
def main(path: pathlib.Path, *args, **kwargs):
    print(path, type(path))

fire.Fire(main)

'''
python test_fire.py "/some_path_string"

/some_path_string <class 'pathlib.WindowsPath'>
'''
```
