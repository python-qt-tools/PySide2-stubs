from typing_extensions import assert_type
from typing import List

from PySide2.QtGui import QPolygon
from PySide2.QtCore import QPoint

point = QPoint()

point_list = [point]

polygon = QPolygon()    # type: QPolygon
polygon << point
polygon << point << point
polygon << [point, point]
polygon << [point, point] << [point, point]

assert type(polygon << point) == QPolygon
assert_type(polygon << point, QPolygon)

assert type(polygon << [point]) == QPolygon
assert_type(polygon << [point], QPolygon)

point_list = polygon + [point]
assert type(point_list) == list
assert type(point_list[0]) == QPoint
assert_type(polygon + [point], List[QPoint])

polygon += point
assert type(polygon) == QPolygon

