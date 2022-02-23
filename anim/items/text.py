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
        super().__init__(label, None)
        if isinstance(pos, relative_point):
            self._pos = relative_point(pos._origin, pos._start_pos)
        else:
            self._pos = relative_point(pos)
        self.set_serif_font(font_size)
        self._pos.add_user(self)
        if fixed_size:
            self.set_fixed_size()
        self._update_geometry()

    def set_font(self, font_name, font_size: float) -> _QGraphicsSimpleTextItem:
        """
        Sets the font name and floating-point font size of the text.
        """
        font = _QFont(font_name)
        font.setPointSizeF(max(0.5, font_size))
        self.setFont(font)
        return self

    def get_font_size(self) -> float:
        """
        Retrieves the floating-point font size of the text.
        """
        return self.font().pointSizeF()

    def get_font_name(self) -> str:
        """
        Retrieves the font name of the text.
        """
        return self.font().name()

    def set_fixed_size(self):
        """
        Sets the font name and floating-point font size of the text.
        """
        self.setFlag(_QGraphicsSimpleTextItem.ItemIgnoresTransformations)

    def set_serif_font(self, font_size: float = 10.) -> _QGraphicsSimpleTextItem:
        """
        Uses a serif font with the given floating-point font size for  the text.
        """
        return self.set_font("Georgia", font_size)

    def set_sans_font(self, font_size: float = 10.) -> _QGraphicsSimpleTextItem:
        """
        Uses a sans-serif font with the given floating-point font size for the text.
        """
        return self.set_font("Trebuchet MS", font_size)

    def center_on(self, other: item) -> _QGraphicsSimpleTextItem:
        """
        Centers the text on the given item.
        """
        self_rect = self.scene_rect()
        other_rect = other.scene_rect()
        self_center = self_rect.center()
        other_center = other_rect.center()
        delta = other_center - self_center
        self._pos.set_absolute_point(self._pos + delta)
        return self

    _quadrant_to_rect_pos = [
        lambda r: (r.topRight() + r.bottomRight()) / 2,
        lambda r: r.topRight(),
        lambda r: (r.topRight() + r.topLeft()) / 2,
        lambda r: r.topLeft(),
        lambda r: (r.topLeft() + r.bottomLeft()) / 2,
        lambda r: r.bottomLeft(),
        lambda r: (r.bottomLeft() + r.bottomRight()) / 2,
        lambda r: r.bottomRight(),
    ]

    def place_around(self, pt: static_point, angle_from_point: float) -> _QGraphicsSimpleTextItem:
        """
        Places the text around the given point in the given direction from the point, in degrees.
        Zero degress is on the right, and turns counter-clockwise.
        """
        rect = self.scene_rect()
        quadrant = (359 - (round(angle_from_point + 337.5) % 360)) // 45
        rect_pos_func = scaling_text._quadrant_to_rect_pos[quadrant]
        delta = pt - rect_pos_func(rect)
        self._pos.set_absolute_point(self._pos + delta)
        return self

    def place_above(self, pt: static_point) -> _QGraphicsSimpleTextItem:
        """
        Places the text above the given point.
        """
        return self.place_around(pt, 90)

    def exponent_pos(self) -> relative_point:
        """
        Retrieves the position of exponent (top-right) of the text.
        """
        corner = self.scene_rect().topRight()
        delta = corner - self._pos
        return relative_point(self._pos, delta)

    def subscript_pos(self) -> relative_point:
        """
        Retrieves the position of subscript (bottom-right) of the text.
        """
        corner = self.sceneBoundingRect().bottomRight()
        delta = corner - self._pos
        return relative_point(self._pos, delta)

    def top_left(self) -> relative_point:
        """
        Retrieves the top-left corner of the text.
        """
        corner = self.sceneBoundingRect().topLeft()
        delta = corner - self._pos
        return relative_point(self._pos, delta)

    def scene_rect(self) -> static_rectangle:
        """
        Retrieves the scene-scale dimension of the text.
        """
        return self.sceneBoundingRect()

    def _update_geometry(self):
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
