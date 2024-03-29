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
    def __init__(self, label: str, pos: point, font_size: float = 10., is_bold: bool = False) -> None:
        super().__init__(label, None)
        if isinstance(pos, relative_point):
            self.position = relative_point(pos.origin, pos.delta)
        else:
            self.position = relative_point(pos)
        self.set_serif_font(font_size, is_bold)
        self.position.add_user(self)
        self.alignment = static_point(0., 0.)
        self._update_geometry()

    def set_alignment(self, alignment: static_point) -> _QGraphicsSimpleTextItem:
        """
        Sets how the width and height of the text affects the position.
        Defaults to top-left.

        For example:
            - 0., 0.    -> top-left
            - 1/2, 1/2  -> center
            - 0., 1./2  -> left-center
            - 1., 1.    -> bottom-right
        """
        self.alignment = alignment
        return self

    def align_on_center(self):
        """
        Align the text on its center.
        """
        return self.set_alignment(static_point(0.5, 0.5))

    def align_on_left(self):
        """
        Align the text on its left.
        """
        return self.set_alignment(static_point(0., 0.5))

    def set_font(self, font_name, font_size: float, is_bold: bool = False) -> _QGraphicsSimpleTextItem:
        """
        Sets the font name and floating-point font size of the text.
        """
        font = _QFont(font_name)
        font.setPointSizeF(max(0.5, font_size))
        font.setBold(is_bold)
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

    def set_serif_font(self, font_size: float = 10., is_bold: bool = False) -> _QGraphicsSimpleTextItem:
        """
        Uses a serif font with the given floating-point font size for  the text.
        """
        return self.set_font("Georgia", font_size, is_bold)

    def set_sans_font(self, font_size: float = 10., is_bold: bool = False) -> _QGraphicsSimpleTextItem:
        """
        Uses a sans-serif font with the given floating-point font size for the text.
        """
        return self.set_font("Trebuchet MS", font_size, is_bold)

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

    def middle_right(self):
        """
        Retrieves the middle-right of the text.
        """
        rect = self.scene_rect()
        corner = (rect.topRight() + rect.bottomRight()) / 2.
        delta = corner - self.position
        return relative_point(self.position, delta)

    def middle_left(self):
        """
        Retrieves the middle-left of the text.
        """
        rect = self.scene_rect()
        corner = (rect.topLeft() + rect.bottomLeft()) / 2.
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
        rect = self.scene_rect()
        new_pos = self.position - static_point(rect.width() * self.alignment.x(), rect.height() * self.alignment.y())
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

    def set_font(self, font_name, font_size: float, is_bold: bool = False) -> scaling_text:
        """
        Sets the font name and floating-point font size of the text.
        """
        super().set_font(font_name, font_size, is_bold)
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
        lineCount = max(1, len(lines))
        letter_count = max([self.min_line_length] + [len(line) for line in lines])

        self._real_rect.setRect(0., 0., int(letter_width * letter_count), letter_height * lineCount)
