import shiboken2
from PySide2.QtWidgets import QWidget


window = QWidget()
window.setObjectName("My Window")
window_ptr: int = shiboken2.getCppPointer(window)[0]
wrapped_window: QWidget = shiboken2.wrapInstance(window_ptr, QWidget)

assert wrapped_window.objectName() == window.objectName()
assert isinstance(wrapped_window, QWidget)
