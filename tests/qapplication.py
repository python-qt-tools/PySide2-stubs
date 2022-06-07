from typing import Any, cast

from PySide2.QtWidgets import QApplication

def slotAppStateChanged(*args: Any) -> None:
    pass

app = cast(QApplication, QApplication.instance())
app.applicationStateChanged.connect(slotAppStateChanged)