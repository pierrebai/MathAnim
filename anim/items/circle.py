from ..point import point

from PySide6.QtWidgets import QGraphicsEllipseItem
from PySide6.QtCore import QRectF, QPointF

import math

class _circle_base(QGraphicsEllipseItem):
    """
    A circle graphics item that is dynamically updated when points defining it move.
    """
    def __init__(self, parent = None):
        super().__init__(parent)

    def update_circle_geometry(self, center: QPointF, radius: float):
        """
        Updates the circle geometry after the points defining it moved.
        """
        diameter = radius * 2.0
        current_rect = QRectF(center.x() - radius, center.y() - radius, diameter, diameter)
        if current_rect != self.rect():
            self.prepareGeometryChange()
            self.setRect(current_rect)

class circle(_circle_base):
    """
    A circle graphics item that is dynamically updated when the center-point or radius move.
    """
    def __init__(self, center: point, radius: float, parent = None):
        super().__init__(parent)
        self.center = center
        self.radius = radius
        center.add_user(self)
        self.update_geometry()

    def update_geometry(self):
        """
        Updates the circle geometry after the center-point or radius moved.
        """
        self.update_circle_geometry(self.center, self.radius)

class diameter_circle(_circle_base):
    """
    A circle graphics item that is dynamically updated when its diameter end-points move.
    """
    def __init__(self, diam_p1: point, diam_p2: point, parent = None):
        super().__init__(parent)
        self.diameter_p1 = diam_p1
        self.diameter_p2 = diam_p2
        diam_p1.add_user(self)
        diam_p2.add_user(self)
        self.update_geometry()

    def update_geometry(self):
        """
        Updates the circle geometry after its diameter end-points moved.
        """
        p1 = self.diameter_p1
        p2 = self.diameter_p2
        center = (p1 + p2) * 0.5
        dx2 = (center.x() - p2.x()) ** 2
        dy2 = (center.y() - p2.y()) ** 2
        radius = math.sqrt(dx2 + dy2)

        self.update_circle_geometry(center, radius)

class radius_circle(_circle_base):
    """
    A circle graphics item that is dynamically updated when its radius end-points move.
    """
    def __init__(self, center: point, radius_point: point, parent = None):
        super().__init__(parent)
        self.center = center
        self.radius_point = radius_point
        center.add_user(self)
        radius_point.add_user(self)
        self.update_geometry()

    def update_geometry(self):
        """
        Updates the circle geometry after its diameter end-points moved.
        """
        center = self.center
        rad_pt = self.radius_point
        dx2 = (center.x() - rad_pt.x()) ** 2
        dy2 = (center.y() - rad_pt.y()) ** 2
        radius = math.sqrt(dx2 + dy2)

        self.update_circle_geometry(center, radius)
