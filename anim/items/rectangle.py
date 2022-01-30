from .point import point

from PySide6.QtWidgets import QGraphicsRectItem
from PySide6.QtCore import QRectF, QPointF

class rectangle(QGraphicsRectItem):
    """
    A rectangle graphics item that is dynamically updated when the two corner points move.
    """
    def __init__(self, p1: point, p2: point, parent = None):
        super().__init__(parent)
        self.p1 = p1
        self.p2 = p2
        p1.add_user(self)
        p2.add_user(self)
        self.update_geometry()

    def update_geometry(self):
        """
        Updates the rectangle geometry after the corner points moved.
        """
        current_rect = QRectF(self.p1, self.p2)
        if current_rect != self.rect():
            self.prepareGeometryChange()
            self.setRect(current_rect)

class center_rectangle(QGraphicsRectItem):
    """
    A rectangle graphics item that is dynamically updated when its center point moves.
    """
    def __init__(self, center: point, half_width: float, half_height: float, parent = None):
        super().__init__(parent)
        self.center = center
        self.corner_delta = QPointF(half_width, half_height)
        center.add_user(self)
        self.update_geometry()

    def update_geometry(self):
        """
        Updates the rectangle geometry after the center point moved.
        """
        current_rect = QRectF(self.center - self.corner_delta, self.center + self.corner_delta)
        if current_rect != self.rect():
            self.prepareGeometryChange()
            self.setRect(current_rect)
