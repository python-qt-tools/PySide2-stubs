from PySide2.QtCore import Qt
from PySide2.QtWidgets import QSpinBox, QFormLayout, QGraphicsView, QLineEdit, QLabel, QLayout, QLayoutItem, QProgressBar, \
    QScrollArea, QTextEdit

a = QSpinBox()
a.setAlignment(Qt.AlignRight)

b = QGraphicsView()
b.setAlignment(Qt.AlignRight)

l = QLabel()
l.setAlignment(Qt.AlignRight)

d = QLineEdit()
d.setAlignment(Qt.AlignRight)

pb = QProgressBar()
pb.setAlignment(Qt.AlignRight)

sa = QScrollArea()
sa.setAlignment(Qt.AlignRight)

te = QTextEdit()
te.setAlignment(Qt.AlignRight)

fl = QFormLayout()
fl.setFormAlignment(Qt.AlignRight)
fl.setAlignment(Qt.AlignRight)
fl.setAlignment(fl, Qt.AlignRight)
fl.setAlignment(b, Qt.AlignRight)

