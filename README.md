# typedargs

A command line parser for typing generation.

## USAGE

```python
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
```

```
$ python example.py -h
usage: example.py [-h] [--debug] [--cache_dir CACHE_DIR] [--host HOST] [--port PORT] app

options for run server

positional arguments:
  app

optional arguments:
  -h, --help            show this help message and exit
  --debug
  --cache_dir CACHE_DIR
  --host HOST
  --port PORT
$ python example.py myapp
ServerOptions(app='myapp', debug=False, cache_dir=None, host='0.0.0.0', port=8080)
$ python example.py myapp --host 127.0.0.1 --debug --port 5000 --cache_dir "static/" --cache_dir "images/"
ServerOptions(app='myapp', debug=True, cache_dir=['static/', 'images/'], host='127.0.0.1', port=5000)
```
