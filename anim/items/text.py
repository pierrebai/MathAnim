from anim.items.rectangle import static_rectangle
from .point import point, relative_point, static_point
from .item import item

from PySide6.QtWidgets import QGraphicsSimpleTextItem as _QGraphicsSimpleTextItem
from PySide6.QtGui import QFont as _QFont

import math
from typing import List as _List

class scaling_text(_QGraphicsSimpleTextItem, item):
    """
    Text graphics item that follows the scene.
    """
    def __init__(self, label: str, pos: point, font_size: float = 10., fixed_size = False) -> None:
        super().__init__(label, None)
        if isinstance(pos, relative_point):
            self.position = relative_point(pos.origin, pos._start_pos)
        else:
            self.position = relative_point(pos)
        self.set_serif_font(font_size)
        self.position.add_user(self)
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
        return self.font().family()

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
        self.position.set_absolute_point(self.position + delta)
        return self

    def place_around(self, pt: static_point, angle_from_point: float, distance_from_point: float) -> _QGraphicsSimpleTextItem:
        """
        Places the text around the given point in the given direction from the point, in radians.
        Zero is on the right, and turns clockwise.
        """
        self.position.set_absolute_point(self.place_around_pos(pt, angle_from_point, distance_from_point))
        return self

    def place_above(self, pt: static_point, distance_from_point: float = 0) -> _QGraphicsSimpleTextItem:
        """
        Places the text above the given point.
        """
        self.position.set_absolute_point(self.place_above_pos(pt, distance_from_point))
        return self

    def place_above_pos(self, pt: static_point, distance_from_point: float = 0) -> relative_point:
        """
        Retrieves the position above the given point.
        """
        return self.place_around_pos(pt, 3 * math.pi / 2, distance_from_point + self.scene_rect().height() / 2)
        
    def place_around_pos(self, pt: static_point, angle_from_point: float, distance_from_point: float) -> relative_point:
        """
        Retrieves the position around the given point in the given direction from the point, in radians.
        Zero is on the right, and turns clockwise.
        """
        while angle_from_point < 0:
            angle_from_point += 2 * math.pi

        dist = static_point(math.cos(angle_from_point), math.sin(angle_from_point)) * distance_from_point

        rect = self.scene_rect()

        delta = pt + dist- rect.center()
        return relative_point(self.position, delta)

    def exponent_pos(self) -> relative_point:
        """
        Retrieves the position of exponent (top-right) of the text.
        """
        corner = self.scene_rect().topRight()
        delta = corner - self.position
        return relative_point(self.position, delta)

    def subscript_pos(self) -> relative_point:
        """
        Retrieves the position of subscript (bottom-right) of the text.
        """
        corner = self.sceneBoundingRect().bottomRight()
        delta = corner - self.position
        return relative_point(self.position, delta)

    def top_left(self) -> relative_point:
        """
        Retrieves the top-left corner of the text.
        """
        corner = self.sceneBoundingRect().topLeft()
        delta = corner - self.position
        return relative_point(self.position, delta)

    def get_all_points(self) -> _List[point]:
        """
        Retrieve all animatable points in the item.
        """
        return [self.position]

    def scene_rect(self) -> static_rectangle:
        """
        Retrieves the scene-scale dimension of the text.
        """
        return self.sceneBoundingRect()

    def _update_geometry(self):
        """
        Updates the text position after the point moved.
        """
        if self.position != self.scenePos():
            self.prepareGeometryChange()
            self.setPos(self.position)


class fixed_size_text(scaling_text):
    """
    Text graphics item that ignores the scene transformation.
    """
    def __init__(self, text: str, pos: point, font_size: float = 10.) -> None:
        super().__init__(text, pos, font_size, True)
