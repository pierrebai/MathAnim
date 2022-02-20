from .point import point, relative_point, static_point
from .item import item
from .rectangle import static_rectangle

from PySide6.QtWidgets import QGraphicsPolygonItem as _QGraphicsPolygonItem
from PySide6.QtGui import QPolygonF as _QPolygonF

from typing import List

static_polygon = _QPolygonF

class polygon(_QGraphicsPolygonItem, item):
    """
    A polygon graphics item that is dynamically updated when its points move.
    """
    def __init__(self, points: List[point]):
        super().__init__(None)
        self.points = points
        for pt in points:
            pt.add_user(self)
        self.update_geometry()

    def center(self) -> relative_point:
        if not self.points:
            return relative_point(point(0., 0))
        center = static_point(0., 0.)
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
        corner = static_point(min_x, min_y)
        delta = corner - self.points[0]
        return relative_point(self.points[0], delta)

    def scene_rect(self) -> static_rectangle:
        return self.sceneBoundingRect()        

    def update_geometry(self):
        """
        Updates the polygon geometry.
        """
        current_poly = _QPolygonF(self.points)
        if current_poly != self.polygon():
            self.prepareGeometryChange()
            self.setPolygon(current_poly)
