import argparse
import dataclasses
import operator
import typing

T = typing.TypeVar("T")

def is_list_type(t):
    return hasattr(t, "__args__") and t == typing.List[t.__args__]


class TypedParser(typing.Generic[T]):
    def __init__(self, cls: typing.Type[T]) -> None:
        self._cls = cls
        self._parser = argparse.ArgumentParser(description=cls.__doc__)
        for f in dataclasses.fields(cls):
            if is_list_type(f.type):
                self._parser.add_argument(f"--{f.name}", action="append")
            elif f.default is dataclasses.MISSING and f.type != bool:
                self._parser.add_argument(f.name, type=f.type)
            elif f.type == bool:
                self._parser.add_argument(f"--{f.name}", action="store_true")
            else:
                self._parser.add_argument(f"--{f.name}", type=f.type, default=f.default)

    def parse(self, argv: typing.List[str]) -> T:
        args = vars(self._parser.parse_args(argv))
        return typing.cast(T, self.create(args))

    def create(self, args):
        return self._cls(**args)

    def run(self, func: typing.Callable[[T], None], args: typing.List[str]) -> None:
        func(self.parse(args))


def options(
    cls: typing.Type[T],
) -> typing.Callable[[typing.Callable[[T], None]], typing.Callable[[typing.List[str]], None]]:
    def dec(func: typing.Callable[[T], None]) -> typing.Callable[[typing.List[str]], None]:
        def f(argv: typing.List[str]) -> None:
            TypedParser(cls).run(func, argv)

        return f

    return dec
