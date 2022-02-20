from anim.items.rectangle import static_rectangle
from .point import point, relative_point, static_point
from .item import item

from PySide6.QtWidgets import QGraphicsSimpleTextItem as _QGraphicsSimpleTextItem
from PySide6.QtGui import QFont as _QFont


class scaling_text(_QGraphicsSimpleTextItem, item):
    """
    Text graphics item that follows the scene.
    """
    def __init__(self, label: str, pos: point, font_size: float = 10., fixed_size = False) -> None:
        super().__init__(None)
        if isinstance(pos, relative_point):
            self._pos = relative_point(pos._origin, pos._start_pos)
        else:
            self._pos = relative_point(pos)
        self.set_serif_font(font_size)
        self._pos.add_user(self)
        if fixed_size:
            self.set_fixed_size()
        self.update_geometry()

    def set_font(self, font_name, font_size) -> _QGraphicsSimpleTextItem:
        font = _QFont(font_name)
        font.setPointSizeF(max(0.5, font_size))
        self.setFont(font)
        return self

    def get_font_size(self) -> float:
        return self.font().pointSizeF()

    def get_font_name(self) -> str:
        return self.font().name()

    def set_fixed_size(self):
        self.setFlag(_QGraphicsSimpleTextItem.ItemIgnoresTransformations)

    def set_serif_font(self, font_size: float = 10.) -> _QGraphicsSimpleTextItem:
        return self.set_font("Georgia", font_size)

    def set_sans_font(self, font_size: float = 10.) -> _QGraphicsSimpleTextItem:
        return self.set_font("Trebuchet MS", font_size)

    def center_on(self, other: item) -> _QGraphicsSimpleTextItem:
        self_rect = self.scene_rect()
        other_rect = other.scene_rect()
        self_center = self_rect.center()
        other_center = other_rect.center()
        delta = other_center - self_center
        self._pos.set_absolute_point(self._pos + delta)
        self.update_geometry()
        return self

    def place_above(self, pt: static_point) -> _QGraphicsSimpleTextItem:
        rect = self.scene_rect()
        bottom_center = static_point(rect.center().x(), rect.center().y() + rect.height() / 2)
        delta = pt - bottom_center
        self._pos.set_absolute_point(self._pos + delta)
        self.update_geometry()
        return self

    def exponent_pos(self) -> relative_point:
        corner = self.scene_rect().topRight()
        delta = corner - self._pos
        return relative_point(self._pos, delta)

    def scene_rect(self) -> static_rectangle:
        return self.sceneBoundingRect()

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
    def __init__(self, text: str, pos: point, font_size: float = 10.) -> None:
        super().__init__(text, pos, font_size, True)
