import typing


def is_list_type(t):
    return hasattr(t, "__args__") and t == typing.List[t.__args__]


def argname(s: str) -> str:
    return s.replace("_", "-")
