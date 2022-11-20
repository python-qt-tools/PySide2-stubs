from typing import Optional

from PySide2.QtWidgets import QListWidget, QListWidgetItem

l = QListWidget()

item = QListWidgetItem(l)

# it should be possible to remove the item widget for an item
l.setItemWidget(item, None)


