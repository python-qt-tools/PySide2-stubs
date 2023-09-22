# pyright: strict

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget

window = QWidget()
window.setWindowFlags(Qt.WindowType.Window)
window.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.Tool)
window.setWindowFlag(Qt.WindowType.Window, True)

assert isinstance(Qt.WindowType.Window, Qt.WindowType)
assert isinstance(Qt.WindowType.Window | Qt.WindowType.Tool, Qt.WindowFlags)
assert not issubclass(Qt.WindowType, Qt.WindowFlags)
