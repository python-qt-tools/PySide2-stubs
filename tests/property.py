from PySide2.QtCore import Property, QObject, Signal


class MyObject(QObject):
    def __init__(self, default_value: int = 5):
        super().__init__()
        self._value = default_value

    def _getter(self) -> int:
        return self._value

    def _setter(self, val: int) -> None:
        if self._value != val:
            self._value = val
            self.valueChanged.emit()

    valueChanged = Signal()
    value = Property(int, _getter, _setter, notify=valueChanged)


obj = MyObject()
x: int = obj.value
obj.value = 10

assert obj.value == 10
assert isinstance(MyObject.value, Property)
