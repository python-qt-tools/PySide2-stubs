from PySide2.QtCore import Qt
from PySide2.QtWidgets import QListWidgetItem

a = QListWidgetItem()
a.setData(Qt.UserRole, {1: 11, 2: 22})
_ = a.data(Qt.UserRole)

