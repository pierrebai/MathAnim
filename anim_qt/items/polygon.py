from .concrete_item_qt import concrete_item_qt

from PySide6.QtWidgets import QGraphicsPolygonItem
from PySide6.QtGui import QPolygonF
from PySide6.QtCore import QPointF

class polygon(QGraphicsPolygonItem, concrete_item_qt):
    """
    A polygon graphics item that is dynamically updated when its points move.
    """
    def __init__(self, parent = None):
        super().__init__(parent)

    def update_geometry(self, new_poly):
        """
        Updates the polygon geometry.
        """
        current_poly = QPolygonF([QPointF(pt.x, pt.y) for pt in new_poly.points])
        if current_poly != self.polygon():
            self.prepareGeometryChange()
            self.setPolygon(current_poly)
