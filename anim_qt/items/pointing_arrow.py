from .concrete_item_qt import concrete_item_qt

from PySide6.QtWidgets import QGraphicsPathItem
from PySide6.QtCore import QPointF
from PySide6.QtGui import QPainterPath


class pointing_arrow(QGraphicsPathItem, concrete_item_qt):
    """
    A circular pointing arrow graphics item that is dynamically updated when the two end-points move.
    """
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.arrow_head = None
        self.arrow_tail = None

    def update_geometry(self, new_arrow) -> None:
        """
        Updates the pointing_arrow geometry after the points moved.
        """
        if self.arrow_tail != new_arrow.tail or self.arrow_head != new_arrow.head:
            self.prepareGeometryChange()
            self._create_arrow(new_arrow)

    def _create_arrow(self, new_arrow) -> None:
        """
        Create the curvy arrow using cubic paths.
        """
        arrow_tail = self.arrow_tail = QPointF(new_arrow.tail.x, new_arrow.tail.y)
        arrow_head = self.arrow_head = QPointF(new_arrow.head.x, new_arrow.head.y)
        dir = (arrow_head - arrow_tail) / 20.
        perp = QPointF(dir.y(), -dir.x())
        arrow_path = QPainterPath()

        arrow_tail_target_dist = dir * 1.0
        arrow_tail_back_spike = dir * 1.0

        arrow_body_half_width = perp * 0.5
        arrow_body_curve_dist = perp * 5.0
        arrow_body_control_pos = dir * 10.0

        arrow_head_half_width = perp * 1.5
        arrow_head_back_dist = dir * 2.0
        arrow_head_back_spike = dir * 3.0
        arrow_head_target_dist = dir * 0.3

        arrow_path.moveTo(arrow_tail + arrow_tail_target_dist)

        arrow_path.lineTo( arrow_tail - arrow_body_half_width + arrow_tail_back_spike)
        arrow_path.cubicTo(
            arrow_tail - arrow_body_half_width + arrow_body_control_pos - arrow_body_curve_dist,
            arrow_head - arrow_body_half_width - arrow_body_control_pos - arrow_body_half_width,
            arrow_head - arrow_head_back_dist - arrow_body_half_width)
        arrow_path.lineTo( arrow_head - arrow_head_back_spike - arrow_head_half_width)

        arrow_path.lineTo( arrow_head - arrow_head_target_dist)

        arrow_path.lineTo( arrow_head - arrow_head_back_spike + arrow_head_half_width)
        arrow_path.lineTo( arrow_head - arrow_head_back_dist + arrow_body_half_width)
        arrow_path.cubicTo(
            arrow_head + arrow_body_half_width - arrow_body_control_pos,
            arrow_tail - arrow_body_curve_dist + arrow_body_control_pos ,
            arrow_tail + arrow_body_half_width + arrow_tail_back_spike)

        arrow_path.lineTo( arrow_tail + arrow_tail_target_dist)

        self.setPath(arrow_path)
