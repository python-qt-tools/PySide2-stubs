from PySide2.QtCore import Slot, QObject

class SomeClass(QObject):

    @Slot(str)
    def someMethod(self, stra):
        ...
