from .point import point
from .item import item
from .rectangle import static_rectangle

from PySide6.QtWidgets import QGraphicsPathItem as _QGraphicsPathItem
from PySide6.QtCore import QPointF as _QPointF
from PySide6.QtGui import QPainterPath as _QPainterPath


class pointing_arrow(_QGraphicsPathItem, item):
    """
    A curvy pointing arrow graphics item that is dynamically updated when the head or tail move.
    """
    def __init__(self, tail: point, head: point) -> None:
        super().__init__(None)
        self.head = None
        self.tail = tail
        self.arrow_head = None
        self.arrow_tail = None
        tail.add_user(self)
        self.set_head(head)

    def set_head(self, new_head):
        """
        Sets a new point to be the head.
        """
        if self.head:
            self.head.remove_user(self)
        self.head = new_head
        new_head.add_user(self)
        self._update_geometry()
        return self

    def set_tail(self, new_tail):
        """
        Sets a new point to be the tail.
        """
        if self.tail:
            self.tail.remove_user(self)
        self.tail = new_tail
        new_tail.add_user(self)
        self._update_geometry()
        return self

    def scene_rect(self) -> static_rectangle:
        return self.sceneBoundingRect()        

    def _update_geometry(self) -> None:
        """
        Updates the pointing_arrow geometry after the points moved.
        """
        if self.arrow_tail != self.tail or self.arrow_head != self.head:
            self.prepareGeometryChange()
            self._create_arrow()

    def _create_arrow(self) -> None:
        """
        Create the curvy arrow using cubic paths.
        """
        arrow_tail = self.arrow_tail = _QPointF(self.tail)
        arrow_head = self.arrow_head = _QPointF(self.head)
        dir = (arrow_head - arrow_tail) / 20.
        perp = _QPointF(dir.y(), -dir.x())
        arrow_path = _QPainterPath()

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
