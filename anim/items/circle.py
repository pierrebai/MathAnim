from .point import point

from PyQt5.QtWidgets import QGraphicsEllipseItem
from PyQt5.QtCore import QRectF

import math

class circle(QGraphicsEllipseItem):
    def __init__(self, center: point, radius: float, parent = None):
        super().__init__(parent)
        self.center = center
        self.radius = radius
        center.add_user(self)
        self.update_geometry()

    def update_geometry(self):
        diameter = 2 * self.radius
        current_rect = QRectF(self.center.x() - self.radius, self.center.y() - self.radius, diameter, diameter)
        if current_rect != self.rect():
            self.prepareGeometryChange()
            self.setRect(current_rect)
            # self.update()
