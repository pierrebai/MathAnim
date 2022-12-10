from anim.items.rectangle import static_rectangle
from .point import point, relative_point, static_point
from .item import item

from PySide6.QtWidgets import QGraphicsSimpleTextItem as _QGraphicsSimpleTextItem
from PySide6.QtGui import QFont as _QFont, QFontMetricsF as _QFontMetricsF
from PySide6.QtCore import QRectF as _QRectF

import math
from typing import List as _List, Tuple as _Tuple

class scaling_text(_QGraphicsSimpleTextItem, item):
    """
    Text graphics item that follows the scene.
    """
    def __init__(self, label: str, pos: point, font_size: float = 10.) -> None:
        super().__init__(label, None)
        if isinstance(pos, relative_point):
            self.position = relative_point(pos.origin, pos._start_pos)
        else:
            self.position = relative_point(pos)
        self.set_serif_font(font_size)
        self.position.add_user(self)
        self.position_on_center = False
        self._update_geometry()

    def set_position_is_center(self, on_center = True) -> _QGraphicsSimpleTextItem:
        """
        Sets that the position is the position of the center of the text.
        Otherwise, the position is the top-left.
        """
        self.position_on_center = on_center
        return self

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

        delta = pt + dist - rect.center()
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
        corner = self.scene_rect().bottomRight()
        delta = corner - self.position
        return relative_point(self.position, delta)

    def top_left(self) -> relative_point:
        """
        Retrieves the top-left corner of the text.
        """
        corner = self.scene_rect().topLeft()
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

        if self.position_on_center:
            new_pos = self.position - static_point(self.scene_rect().width() / 2., self.scene_rect().height() / 2.)
        else:
            new_pos = self.position
        if new_pos != self.scenePos():
            self.prepareGeometryChange()
            self.setPos(new_pos)

class fixed_size_text(scaling_text):
    """
    Text graphics item that ignores the scene transformation.
    """
    def __init__(self, text: str, pos: point, font_size: float = 10., min_line_length: int = 36) -> None:
        self.min_line_length = min_line_length
        self._real_rect = static_rectangle(0, 0, 6, 2)
        self.letter_width = 1.
        self.letter_height = 1.
        super().__init__(text, pos, font_size)
        self.setFlag(_QGraphicsSimpleTextItem.ItemIgnoresTransformations)
        self._update_letter_size()

    def set_font(self, font_name, font_size: float) -> scaling_text:
        """
        Sets the font name and floating-point font size of the text.
        """
        super().set_font(font_name, font_size)
        return self._update_letter_size()

    def _update_letter_size(self) -> scaling_text:
        self.letter_width = _QFontMetricsF(self.font()).averageCharWidth()
        self.letter_height = _QFontMetricsF(self.font()).height()
        return self

    def scene_rect(self) -> static_rectangle:
        """
        Retrieves the scene-scale dimension of the text.
        """
        return self.mapRectToScene(self._real_rect.x(), self._real_rect.y(), self._real_rect.width(), self._real_rect.height())

    def pos(self) -> static_point:
        pos = super().pos()
        pos = self.transform().map(pos)
        return pos

    def scenePos(self) -> static_point:
        pos = super().scenePos()
        pos = self.transform().map(pos)
        return pos

    def boundingRect(self):
        return self._real_rect

    def sceneBoundingRect(self):
        return self._real_rect

    def setText(self, text: str) -> None:
        super().setText(text)
        self._update_geometry()

    def _get_scaling(self) -> _Tuple[float, float]:
        '''
        Retrieve the scaling of the view, rounded to the nearest quarter.
        The rounding is to give some stability, avoiding constant small
        shifts.
        '''
        sx = sy = 1.
        scene = self.scene()
        if scene:
            views = scene.views()
            if views and views[0]:
                sz = views[0].transform().mapRect(_QRectF(0., 0., 1., 1.)).size()
                sx, sy = 1. / sz.width(), 1. / sz.height()
                sx = round(sx * 2.) / 2.
                sy = round(sy * 2.) / 2.
        return sx, sy

    def _update_geometry(self):
        """
        Updates the text position after the point moved.
        """
        pos = self.transform().map(self.position)
        if pos != self.scenePos():
            self.prepareGeometryChange()
            self.setPos(pos)

        self.prepareGeometryChange()
        sx, sy = self._get_scaling()
        letter_width  = self.letter_width  * sx
        letter_height = self.letter_height * sy

        lines = self.text().splitlines()
        lineCount = len(lines)
        letter_count = max([self.min_line_length] + [len(line) for line in lines])

        self._real_rect.setRect(0., 0., int(letter_width * letter_count), letter_height * lineCount)
