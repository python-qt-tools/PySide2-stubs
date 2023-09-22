import enum
import typing_extensions

from PySide2.QtCore import QObject, QEnum, QFlag


class Demo(QObject):
    @QEnum
    class Orientation(enum.Enum):
        North, East, South, West = range(4)

    @QEnum
    class State(enum.IntEnum):
        SUCCESS = enum.auto()
        ERROR = enum.auto()

    @QFlag
    class Color(enum.Flag):
        RED = enum.auto()
        BLUE = enum.auto()
        GREEN = enum.auto()
        WHITE = RED | BLUE | GREEN


enum_value: enum.Enum = Demo.Orientation.East
flag_value: enum.Flag = Demo.Color.WHITE
int_value: int = Demo.State.ERROR

assert issubclass(Demo.Orientation, enum.Enum)
assert issubclass(Demo.Color, enum.Flag)
assert issubclass(Demo.State, int)
assert Demo.State.SUCCESS == 1
assert Demo.Color.BLUE.value == 2
assert isinstance(Demo.Color.GREEN, Demo.Color)
