from typing_extensions import assert_type
from PySide2.QtCore import QTimer, Signal, SignalInstance

assert_type(QTimer.timeout, Signal)

timer = QTimer()
assert_type(timer.timeout, SignalInstance)

timer.timeout.connect(lambda: None)
