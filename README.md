# TypeFire

 [![CodeFactor](https://www.codefactor.io/repository/github/luxuncang/typefire/badge)](https://www.codefactor.io/repository/github/luxuncang/typefire)
 [![GitHub](https://img.shields.io/github/license/luxuncang/typefire)](https://github.com/luxuncang/typefire/blob/master/LICENSE)
 [![CodeQL](https://github.com/luxuncang/typefire/workflows/CodeQL/badge.svg)](https://github.com/luxuncang/typefire/blob/main/.github/workflows/codeql-analysis.yml)

**通过装饰器零入侵性的，对 `fire-python` 的类型约束进行拓展，此外其还适用于任何函数对象进行基于注解的类型转换**

## 安装

```bash
pip install typefire
```

## 特性
- 支持注解类型转换
- 支持 async/await
- 零入侵性

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
from typefire import Switch, TypeFire, typefire, typeswitch
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

```python
from typefire import Switch, TypeFire, typefire, typeswitch
import fire
import pathlib

TypeFire.add_switch(Switch(str, pathlib.Path, lambda p: pathlib.Path(p)))

@typefire
def main(path: pathlib.Path, *args, **kwargs):
    print(path, type(path))

main("/some_path_string")
main("--path=/some_path_string")
```
