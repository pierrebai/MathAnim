from .concrete_item_qt import concrete_item_qt

from PySide6.QtWidgets import QGraphicsEllipseItem
from PySide6.QtCore import QRectF


class circle(QGraphicsEllipseItem, concrete_item_qt):
    """
    A circle graphics item.
    """
    def __init__(self, parent = None):
        super().__init__(parent)

    def update_geometry(self, new_circle):
        """
        Updates the circle geometry if the rectangle changed.
        """
        center, radius = new_circle.get_center_and_radius()
        diameter = radius * 2.0
        current_rect = QRectF(center.x - radius, center.y - radius, diameter, diameter)
        if current_rect != self.rect():
            self.prepareGeometryChange()
            self.setRect(current_rect)
