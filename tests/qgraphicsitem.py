from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGraphicsItem

class TestItem(QGraphicsItem):
	pass

a = TestItem()
a.setData(Qt.UserRole, {1: 11, 2: 22})
_ = a.data(Qt.UserRole)

a.setFlags(QGraphicsItem.ItemSendsScenePositionChanges)