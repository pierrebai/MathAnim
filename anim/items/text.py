from .point import point, relative_point

from PySide6.QtWidgets import QGraphicsSimpleTextItem, QGraphicsItem
from PySide6.QtGui import QFont

class scaling_text(QGraphicsSimpleTextItem):
    """
    Text graphics item that follows the scene.
    """
    def __init__(self, label: str, pos: point, font_size: float = 10., parent = None) -> None:
        super().__init__(label, parent)
        if isinstance(pos, relative_point):
            self._pos = relative_point(pos._origin, pos._start_pos)
        else:
            self._pos = relative_point(pos)
        self.set_serif_font(font_size)
        self._pos.add_user(self)
        self.update_geometry()

    def set_font(self, font_name, font_size) -> QGraphicsSimpleTextItem:
        font = QFont(font_name)
        font.setPointSizeF(max(0.5, font_size))
        self.setFont(font)
        return self

    def set_serif_font(self, font_size: float = 10.) -> QGraphicsSimpleTextItem:
        return self.set_font("Georgia", font_size)

    def set_sans_font(self, font_size: float = 10.) -> QGraphicsSimpleTextItem:
        return self.set_font("Trebuchet MS", font_size)

    def get_font_size(self) -> float:
        return self.font().pointSizeF()

    def center_on(self, other: QGraphicsItem) -> QGraphicsSimpleTextItem:
        self_rect = self.sceneBoundingRect()
        other_rect = other.sceneBoundingRect()
        self_center = self_rect.center()
        other_center = other_rect.center()
        delta = other_center - self_center
        self._pos.set_absolute_point(self._pos + delta)
        self.update_geometry()
        return self

    def place_above(self, pt: point) -> QGraphicsSimpleTextItem:
        rect = self.sceneBoundingRect()
        bottom_center = point(rect.x() + rect.width() / 2, rect.y() + rect.height())
        delta = pt - bottom_center
        self._pos.set_absolute_point(self._pos + delta)
        self.update_geometry()
        return self

    def exponent_pos(self) -> relative_point:
        corner = self.sceneBoundingRect().topRight()
        delta = corner - self._pos
        return relative_point(self._pos, delta)

    def subscript_pos(self) -> relative_point:
        corner = self.sceneBoundingRect().bottomRight()
        delta = corner - self._pos
        return relative_point(self._pos, delta)

    def top_left(self) -> relative_point:
        corner = self.sceneBoundingRect().topLeft()
        delta = corner - self._pos
        return relative_point(self._pos, delta)

    def update_geometry(self):
        """
        Updates the text position after the point moved.
        """
        if self._pos != self.scenePos():
            self.prepareGeometryChange()
            self.setPos(self._pos)

class fixed_size_text(scaling_text):
    """
    Text graphics item that ignores the scene transformation.
    """
    def __init__(self, text: str, pos: point, font_size: float = 10., parent = None) -> None:
        super().__init__(text, pos, font_size, parent)
        self.setFlag(QGraphicsSimpleTextItem.ItemIgnoresTransformations)
