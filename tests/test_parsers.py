import dataclasses
import typing
import pytest


class TestTypedParser:
    @pytest.fixture
    def target(self):
        from typedargs.parsers import TypedParser

        return TypedParser

    def test_init(self, target, mocker):
        mock_parser_cls = mocker.patch("typedargs.parsers.argparse.ArgumentParser")
        mock_parser = mock_parser_cls.return_value
        @dataclasses.dataclass
        class Dummy:
            """this is dummy"""

            str_args: str
            appendable_options: typing.List[str]
            bool_switch: bool

        parser = target(Dummy)
        assert parser._parser == mock_parser
        mock_parser_cls.assert_called_with(description="this is dummy")
        assert mock_parser.add_argument.mock_calls == [
            mocker.call("str_args", type=str),
            mocker.call("--appendable-options", action="append"),
            mocker.call("--bool-switch", action="store_true"),
        ]
