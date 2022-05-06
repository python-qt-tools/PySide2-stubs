from typing import List, Iterable
from typing_extensions import assert_type

from PySide2.QtCore import QObject
from PySide2.QtWidgets import QWidget, QApplication

if __name__ == '__main__':
    app = QApplication([])

o1 = QWidget()
o2 = QWidget(o1)
o3 = QObject(o1)

a = o1.findChildren(QObject)
assert_type(a, List[QObject])
assert type(a) == list
assert isinstance(a[0], QObject)

b = o1.findChildren(QWidget)
assert_type(b, List[QWidget])
assert type(b) == list
assert isinstance(b[0], QWidget)

c: List[QWidget]
c = o1.findChildren(QObject, '')

d: List[QObject]
d = o1.findChildren(QWidget, '')

