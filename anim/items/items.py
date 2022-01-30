from PySide6.QtGui import QBrush as _QBrush, QColor as _QColor, QPen as _QPen
from PySide6.QtWidgets import QGraphicsItem as _QGraphicsItem, QGraphicsRectItem as _QGraphicsRectItem

from .circle import circle, radius_circle, diameter_circle
from .line import line
from .polygon import polygon
from .rectangle import rectangle, center_rectangle
from .pointing_arrow import pointing_arrow
from .point import point, relative_point

from typing import List as _List

"""
Helpers to create various kind of scene items.
"""

outer_size = 1000.
line_width = outer_size / 50.
dot_size = line_width * 1.5
tile_size = outer_size / 100.

no_color = _QColor(0, 0, 0, 0)

orange_color    = _QColor(235, 180,  40, 220)
blue_color      = _QColor( 68, 125, 255, 200)
green_color     = _QColor( 83, 223,  56, 200)
black_color     = _QColor(  0,   0,   0)
cyan_color      = _QColor( 30, 190, 220)
gray_color      = _QColor(220, 220, 220, 120)
red_color       = _QColor(255,  84,  46)

dark_orange_color   = orange_color.darker(130)
dark_blue_color     = blue_color.darker(130)
dark_green_color    = green_color.darker(130)
dark_cyan_color     = cyan_color.darker(130)
dark_gray_color     = gray_color.darker(130)
dark_red_color      = red_color.darker(130)

pale_blue_color     = blue_color.lighter(130); pale_blue_color.setAlpha(120)

no_pen   = _QPen(no_color, 0)
no_brush = _QBrush(no_color)


cross_points = [
        point(1, 3), point(3, 1), point(tile_size / 2, 3),
        point(tile_size - 3, 1), point(tile_size - 1, 3), point(tile_size - 3, tile_size / 2),
        point(tile_size - 1, tile_size - 3), point(tile_size - 3, tile_size - 1), point(tile_size / 2, tile_size - 3),
        point(3, tile_size - 1), point(1, tile_size - 3), point(3, tile_size / 2),
]

arrow_points = [
    point(2, 5), point(tile_size / 2, 1), point(tile_size - 2, 5),
    point(tile_size / 2 + 1, 4), point(tile_size / 2 + 1, tile_size - 1),
    point(tile_size / 2 - 1, tile_size - 1), point(tile_size / 2 - 1, 4), 
]

def _prepare_item(item: _QGraphicsItem, pen: _QPen, brush_color: _QColor, parent: _QGraphicsItem) -> None:
    item.setPen(pen)
    item.setBrush(_QBrush(brush_color))
    if parent:
        if isinstance(parent, _QGraphicsItem):
            item.setParentItem(parent)
        else:
            item.setParentItem(parent.item)

def create_cross(color: _QColor = red_color, parent: _QGraphicsItem = None) -> polygon:
    item = polygon(cross_points)
    _prepare_item(item, _QPen(color.darker(130), 1), color, parent)
    return item

def create_arrow(rotation_angle, color: _QColor = black_color, parent: _QGraphicsItem = None) -> polygon:
    item = polygon(arrow_points)
    item.setTransformOriginPoint(tile_size / 2, tile_size / 2)
    item.setRotation(rotation_angle)
    _prepare_item(item, no_pen, color, parent)
    return item

def create_circle(center: point, radius: float, color: _QColor = dark_blue_color, thickness = line_width, parent: _QGraphicsItem = None) -> circle:
    """
    Creates a dynamic circle of the given color and thicknes.
    """
    item = circle(center, radius)
    _prepare_item(item, _QPen(color, thickness), no_color, parent)
    return item

def create_disk(center: point, radius: float, color: _QColor = gray_color, parent: _QGraphicsItem = None) -> circle:
    """
    Creates a dynamic filled disk of the given color.
    """
    item = circle(center, radius)
    _prepare_item(item, no_pen, color, parent)
    return item

def create_line(p1: point, p2: point, color: _QColor = green_color, thickness = line_width, parent: _QGraphicsItem = None) -> line:
    """
    Creates a dynamic line of the given color and thicknes.
    """
    item = line(p1, p2)
    _prepare_item(item, _QPen(color, thickness), no_color, parent)
    return item

def create_pointing_arrow(tail: point, head: point, color: _QColor = pale_blue_color, parent: _QGraphicsItem = None) -> line:
    """
    Creates a dynamic pointing arrow of the given color.
    """
    item = pointing_arrow(tail, head)
    _prepare_item(item, no_pen, color, parent)
    return item

def create_rect(x: float, y: float, width: float, height: float, color: _QColor = dark_gray_color, thickness = line_width, parent: _QGraphicsItem = None) -> _QGraphicsRectItem:
    item = _QGraphicsRectItem(0, 0, width, height)
    item.setPos(x, y)
    _prepare_item(item, _QPen(black_color, thickness), color, parent)
    return item

def create_two_points_rect(p1: point, p2: point, color: _QColor = dark_gray_color, thickness = line_width, parent: _QGraphicsItem = None) -> rectangle:
    """
    Creates a dynamic rectangle out of two corners of the given color.
    """
    item = rectangle(p1, p2)
    _prepare_item(item, _QPen(black_color, thickness), color, parent)
    return item

def create_center_rect(p1: point, half_width: float, half_height: float, color: _QColor = dark_gray_color, thickness = line_width, parent: _QGraphicsItem = None) -> rectangle:
    """
    Creates a dynamic rectangle out of its center position and half-width and half-height of the given color.
    """
    item = center_rectangle(p1, half_width, half_height)
    _prepare_item(item, _QPen(black_color, thickness), color, parent)
    return item

def create_polygon(pts: _List[point], color: _QColor = dark_gray_color, thickness = line_width, parent: _QGraphicsItem = None) -> polygon:
    """
    Create a dynamic polygon of the giuven color and line thhicknes.
    """
    item = polygon(pts)
    _prepare_item(item, _QPen(color, thickness), no_color, parent)
    return item
