import dataclasses
import sys
import typing

from typedargs import options


@dataclasses.dataclass
class ServerOptions:
    """options for run server"""

    app: str
    debug: bool
    cache_dir: typing.List[str]
    host: str = dataclasses.field(default="0.0.0.0")
    port: int = dataclasses.field(default=8080)


@options(ServerOptions)
def main(options: ServerOptions) -> None:
    print(options)


if __name__ == "__main__":
    main(sys.argv[1:])
