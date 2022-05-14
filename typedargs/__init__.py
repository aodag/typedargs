import typing
from .parsers import TypedParser

T = typing.TypeVar("T")


def options(
    cls: typing.Type[T],
) -> typing.Callable[
    [typing.Callable[[T], None]], typing.Callable[[typing.List[str]], None]
]:
    def dec(
        func: typing.Callable[[T], None]
    ) -> typing.Callable[[typing.List[str]], None]:
        def f(argv: typing.List[str]) -> None:
            TypedParser(cls).run(func, argv)

        return f

    return dec
