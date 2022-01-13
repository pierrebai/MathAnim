from .point import point

from PyQt5.QtWidgets import QGraphicsPolygonItem
from PyQt5.QtGui import QPolygonF

from typing import List

class polygon(QGraphicsPolygonItem):
    def __init__(self, points: List[point], parent = None):
        super().__init__(parent)
        self.points = points
        for pt in points:
            pt.add_user(self)
        self.update_geometry()

    def update_geometry(self):
        current_poly = QPolygonF(self.points)
        if current_poly != self.polygon():
            self.prepareGeometryChange()
            self.setPolygon(current_poly)
            # self.update()
