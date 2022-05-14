import argparse
import dataclasses
import typing
from .utils import argname, is_list_type

T = typing.TypeVar("T")


class TypedParser(typing.Generic[T]):
    def __init__(self, cls: typing.Type[T]) -> None:
        self._cls = cls
        self._parser = argparse.ArgumentParser(description=cls.__doc__)
        for f in dataclasses.fields(cls):
            name = argname(f.name)
            if is_list_type(f.type):
                self._parser.add_argument(f"--{name}", action="append")
            elif f.default is dataclasses.MISSING and f.type != bool:
                self._parser.add_argument(f.name, type=f.type)
            elif f.type == bool:
                self._parser.add_argument(f"--{name}", action="store_true")
            else:
                self._parser.add_argument(f"--{name}", type=f.type, default=f.default)

    def parse(self, argv: typing.List[str]) -> T:
        args = vars(self._parser.parse_args(argv))
        return self._cls(**args)

    def run(self, func: typing.Callable[[T], None], args: typing.List[str]) -> None:
        func(self.parse(args))
