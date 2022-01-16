from ..point import point

from PySide6.QtWidgets import QGraphicsPathItem
from PySide6.QtCore import QPointF
from PySide6.QtGui import QPainterPath


class pointing_arrow(QGraphicsPathItem):
    """
    A circular pointing arrow graphics item that is dynamically updated when the two end-points move.
    """
    def __init__(self, tail: point, head: point, parent = None) -> None:
        super().__init__(parent)
        self.tail = tail
        self.head = head
        self.arrow_tail = None
        self.arrow_head = None
        tail.add_user(self)
        head.add_user(self)
        self.update_geometry()

    def update_geometry(self) -> None:
        """
        Updates the pointing_arrow geometry after the points moved.
        """
        if self.arrow_tail != self.tail or self.arrow_head != self.head:
            self.prepareGeometryChange()
            self._create_arrow()

    def _create_arrow(self) -> None:
        arrow_tail = self.arrow_tail = QPointF(self.tail)
        arrow_head = self.arrow_head = QPointF(self.head)
        dir = (arrow_head - arrow_tail) / 20.
        perp = QPointF(dir.y(), -dir.x())
        arrow_path = QPainterPath()
        arrow_path.moveTo(arrow_tail + dir)
        arrow_path.lineTo( arrow_tail + dir       + perp * 0.5)
        arrow_path.lineTo( arrow_head - dir * 2.5 + perp * 0.5)
        arrow_path.lineTo( arrow_head - dir * 3.0 + perp * 1.5)
        arrow_path.lineTo( arrow_head - dir * 0.3             )
        arrow_path.lineTo( arrow_head - dir * 3.0 - perp * 1.5)
        arrow_path.lineTo( arrow_head - dir * 2.5 - perp * 0.5)
        arrow_path.lineTo( arrow_tail + dir       - perp * 0.5)
        arrow_path.lineTo( arrow_tail + dir)
        self.setPath(arrow_path)
