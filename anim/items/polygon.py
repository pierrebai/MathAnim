from .point import point, relative_point

from PySide6.QtWidgets import QGraphicsPolygonItem
from PySide6.QtGui import QPolygonF
from PySide6.QtCore import QPointF

from typing import List

class polygon(QGraphicsPolygonItem):
    """
    A polygon graphics item that is dynamically updated when its points move.
    """
    def __init__(self, points: List[point], parent = None):
        super().__init__(parent)
        self.points = points
        for pt in points:
            pt.add_user(self)
        self.update_geometry()

    def update_geometry(self):
        """
        Updates the polygon geometry after the points moved.
        """
        current_poly = QPolygonF(self.points)
        if current_poly != self.polygon():
            self.prepareGeometryChange()
            self.setPolygon(current_poly)

    def center(self) -> relative_point:
        if not self.points:
            return relative_point(point(0., 0))
        center = QPointF(0., 0.)
        for pt in self.points:
            center += pt
        center = center / float(len(self.points))
        delta = center - self.points[0]
        return relative_point(self.points[0], delta)

    def top_left(self) -> relative_point:
        if not self.points:
            return relative_point(point(0., 0))
        min_x = 1000000
        min_y = 1000000
        for pt in self.points:
            min_x = min(pt.x(), min_x)
            min_y = min(pt.y(), min_y)
        corner = QPointF(min_x, min_y)
        delta = corner - self.points[0]
        return relative_point(self.points[0], delta)
