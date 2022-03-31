from typefire import TypeFire, typefire, typeswitch, Agreement, Switch
import fire
import pathlib


def add(x, y):
    return x + y


@typefire(Agreement(Switch(str, pathlib.Path, lambda p: pathlib.Path(p))))
class BrokenCalculator:
    def __init__(self, offset=0):
        self._offset = offset

    def add(self, x, y):
        return x + y + self._offset

    def multiply(self, x, y):
        return x * y + self._offset

    def hint(self, path: pathlib.Path):
        print(path, type(path))
        return path

    @staticmethod
    def static_add(x: str, y: str):
        print(type(x), type(y))
        return x + y

    @classmethod
    def class_add(cls, x: str, y: str):
        return x + y

    @property
    def getoffset(self):
        return self._offset


def test_typefire():
    cmd = "--x=1 --y=2"
    assert typefire()(add)(cmd) == fire.Fire(add, cmd)


def test_typefire_help():
    cmd = "--help"
    assert typefire()(BrokenCalculator)(cmd) == fire.Fire(BrokenCalculator, cmd)


def test_typeswitch():
    @typeswitch(Agreement(Switch(str, pathlib.Path, lambda p: pathlib.Path(p))))
    def main(path: pathlib.Path, *args, **kwargs):
        print(path, type(path))
        return path

    assert main("/Users/joe/Desktop/test.txt") == pathlib.Path(
        "/Users/joe/Desktop/test.txt"
    )


def test_typefire_class():
    cmd = "--offset=1 - add --x=1 --y=2"
    assert typefire()(BrokenCalculator)(cmd) == fire.Fire(BrokenCalculator, cmd)


def test_typefire_class_subclass():
    cmd = "add --x=1 --y=2"
    sub = BrokenCalculator(1)
    assert typefire()(sub)(cmd) == fire.Fire(sub, cmd)


def test_typefire_class_subclass_method():
    cmd = "hint --path=/Users/joe/Desktop/test.txt"
    sub = BrokenCalculator(1)
    agm = Agreement(Switch(str, pathlib.Path, lambda p: pathlib.Path(p)))
    assert typefire(agm)(sub)(cmd) == fire.Fire(sub, cmd)


def test_typefire_class_subclass_method_static():
    cmd = "static_add --x=1 --y=2"
    sub = BrokenCalculator(1)
    agm = Agreement(Switch(int, str, lambda p: str(p)))
    assert typefire(agm)(sub)(cmd) == fire.Fire(sub, cmd)


def test_typefire_class_subclass_method_class():
    cmd = "class_add --x=1 --y=2"
    agm = Agreement(Switch(int, str, lambda p: str(p)))
    assert typefire(agm)(BrokenCalculator)(cmd) == fire.Fire(BrokenCalculator, cmd)


def test_typefire_class_subclass_method_property():
    cmd = "getoffset"
    sub = BrokenCalculator(1)
    # agm = Agreement(Switch(int, str, lambda p: str(p)))
    assert typefire()(sub)(cmd) == fire.Fire(sub, cmd)


# test_typefire()
# test_typefire_help()
# test_typeswitch()
# test_typefire_class()
# test_typefire_class_subclass()
# test_typefire_class_subclass_method()
# test_typefire_class_subclass_method_static()
# test_typefire_class_subclass_method_class()
# test_typefire_class_subclass_method_property()


a = BrokenCalculator(1)
# print(a('add --x=1 --y=2'))