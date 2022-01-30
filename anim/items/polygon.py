from .point import point

from PySide6.QtWidgets import QGraphicsPolygonItem
from PySide6.QtGui import QPolygonF

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
