from ..point import point

from PySide6.QtWidgets import QGraphicsEllipseItem
from PySide6.QtCore import QRectF

class circle(QGraphicsEllipseItem):
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
        diameter = 2 * self.radius
        current_rect = QRectF(self.center.x() - self.radius, self.center.y() - self.radius, diameter, diameter)
        if current_rect != self.rect():
            self.prepareGeometryChange()
            self.setRect(current_rect)
