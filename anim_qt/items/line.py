from .concrete_item_qt import concrete_item_qt

from PySide6.QtWidgets import QGraphicsLineItem
from PySide6.QtCore import QLineF, QPointF

class line(QGraphicsLineItem, concrete_item_qt):
    """
    A line graphics item.
    """
    def __init__(self, parent = None):
        super().__init__(parent)

    def update_geometry(self, new_line):
        """
        Updates the line geometry if the line moved.
        """
        current_line = QLineF(QPointF(new_line.p1.x, new_line.p1.y), QPointF(new_line.p2.x, new_line.p2.y))
        if current_line != self.line():
            self.prepareGeometryChange()
            self.setLine(current_line)
