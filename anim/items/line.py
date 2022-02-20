from .point import point
from .item import item
from .rectangle import static_rectangle

from PySide6.QtWidgets import QGraphicsLineItem as _QGraphicsLineItem
from PySide6.QtCore import QLineF as _QLineF, QPointF as _QPointF


class line(_QGraphicsLineItem, item):
    """
    A line item that is dynamically updated when the two end-points move.
    """
    def __init__(self, p1: point, p2: point):
        super().__init__(None)
        self.p1 = p1
        self.p2 = p2
        p1.add_user(self)
        p2.add_user(self)
        self.update_geometry()

    def scene_rect(self) -> static_rectangle:
        return self.sceneBoundingRect()        

    def update_geometry(self):
        """
        Updates the line geometry if the line moved.
        """
        current_line = _QLineF(_QPointF(self.p1.x(), self.p1.y()), _QPointF(self.p2.x(), self.p2.y()))
        if current_line != self.line():
            self.prepareGeometryChange()
            self.setLine(current_line)
