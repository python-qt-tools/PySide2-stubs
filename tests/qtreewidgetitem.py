from PySide2.QtWidgets import QTreeWidgetItem


class MyTreeWidgetItem(QTreeWidgetItem):

    # add comparison indicator to allow custom sorting of items
    def __lt__(self, other: QTreeWidgetItem) -> bool:
        return super().__lt__(other)

t = QTreeWidgetItem()

b = True    # type: bool
b = t < t
b = t == t
b = t != t
