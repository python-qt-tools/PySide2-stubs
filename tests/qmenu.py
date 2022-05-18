from PySide2.QtWidgets import QMenu

# the default version of pyside2 stubs would not detect missing attributes
# this test verifies that this is fixed

m = QMenu()
try:
    # exec() is actually not available
    m.exec()    # type: ignore[attr-defined]
    assert False, 'Should not reach here'
except AttributeError:
    pass