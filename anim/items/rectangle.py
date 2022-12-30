from .point import point, static_point
from .item import item

from PySide6.QtWidgets import QGraphicsRectItem as _QGraphicsRectItem
from PySide6.QtCore import QRectF as _QRectF, QPointF as _QPointF

from typing import List as _List


static_rectangle = _QRectF

class rectangle(_QGraphicsRectItem, item):
    """
    A rectangle graphics item that is dynamically updated when the two corner points move.
    """
    def __init__(self, p1: point, p2: point):
        super().__init__()
        self.p1 = p1
        self.p2 = p2
        p1.add_user(self)
        p2.add_user(self)
        self._update_geometry()

    def get_all_points(self) -> _List[point]:
        """
        Retrieve all animatable points in the item.
        """
        return [self.p1, self.p2]

    def scene_rect(self) -> static_rectangle:
        return static_rectangle(static_point(self.p1), static_point(self.p2))

    def _update_geometry(self):
        """
        Updates the rectangle geometry after the rectangle points moved.
        """
        current_rect = _QRectF(_QPointF(self.p1.x(), self.p1.y()), _QPointF(self.p2.x(), self.p2.y()))
        if current_rect != self.rect():
            self.prepareGeometryChange()
            self.setRect(current_rect)

class center_rectangle(_QGraphicsRectItem, item):
    """
    A rectangle graphics item that is dynamically updated when its center point moves.
    """
    def __init__(self, center: point, *args):
        super().__init__()
        self.center = center
        self.extent = point(*args)
        center.add_user(self)
        self.extent.add_user(self)
        self._update_geometry()

    def get_all_points(self) -> _List[point]:
        """
        Retrieve all animatable points in the item.
        """
        return [self.center]

    def scene_rect(self) -> static_rectangle:
        corner = self.center - self.extent / 2
        return static_rectangle(corner.x(), corner.y(), self.extent.x(), self.extent.y())

    def _update_geometry(self):
        """
        Updates the rectangle geometry after the rectangle points moved.
        """
        current_rect = self.scene_rect()
        if current_rect != self.rect():
            self.prepareGeometryChange()
            self.setRect(current_rect)
