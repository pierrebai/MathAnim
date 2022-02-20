from .concrete_item_qt import concrete_item_qt

from PySide6.QtWidgets import QGraphicsRectItem
from PySide6.QtCore import QRectF, QPointF

class rectangle(QGraphicsRectItem, concrete_item_qt):
    """
    A rectangle graphics item that is dynamically updated when the two corner points move.
    """
    def __init__(self, parent = None):
        super().__init__(parent)

    def update_geometry(self, new_rect):
        """
        Updates the rectangle geometry after the corner points moved.
        """
        current_rect = QRectF(QPointF(new_rect.p1.x, new_rect.p1.y), QPointF(new_rect.p2.x, new_rect.p2.y))
        if current_rect != self.rect():
            self.prepareGeometryChange()
            self.setRect(current_rect)

