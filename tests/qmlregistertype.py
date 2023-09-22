from PySide2.QtCore import QObject
from PySide2.QtQml import qmlRegisterType


class MyType(QObject):
    pass

qmlRegisterType(MyType, "MyPackage", 1, 0, "MyType")
