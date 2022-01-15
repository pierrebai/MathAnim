from ..point import point

from PySide6.QtWidgets import QGraphicsLineItem
from PySide6.QtCore import QLineF

class line(QGraphicsLineItem):
    """
    A line graphics item that is dynamically updated when the two end-points move.
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
        Updates the line geometry after the points moved.
        """
        current_line = QLineF(self.p1, self.p2)
        if current_line != self.line():
            self.prepareGeometryChange()
            self.setLine(current_line)
