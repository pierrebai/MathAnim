from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtWidgets import QGraphicsItem, QGraphicsRectItem

from .circle import circle
from .line import line
from .polygon import polygon
from ..point import point

from typing import List

"""
Helpers to create various kind of scene items.
"""

outer_size = 1000.
line_width = outer_size / 50.
dot_size = line_width * 1.5
tile_size = outer_size / 100.

no_color = QColor(0, 0, 0, 0)

orange_color    = QColor(235, 180,  40, 220)
blue_color      = QColor( 68, 125, 255, 200)
green_color     = QColor( 83, 223,  56, 200)
black_color     = QColor(  0,   0,   0)
cyan_color      = QColor( 30, 190, 220)
gray_color      = QColor(220, 220, 220, 120)
red_color       = QColor(255,  84,  46)

dark_orange_color   = orange_color.darker(130)
dark_blue_color     = blue_color.darker(130)
dark_green_color    = green_color.darker(130)
dark_cyan_color     = cyan_color.darker(130)
dark_gray_color     = gray_color.darker(130)
dark_red_color      = red_color.darker(130)

no_pen   = QPen(no_color, 0)
no_brush = QBrush(no_color)


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

def _prepare_item(item: QGraphicsItem, pen: QPen, brush_color: QColor, parent: QGraphicsItem) -> None:
    item.setPen(pen)
    item.setBrush(QBrush(brush_color))
    if parent:
        if isinstance(parent, QGraphicsItem):
            item.setParentItem(parent)
        else:
            item.setParentItem(parent.item)

def create_cross(color: QColor = red_color, parent: QGraphicsItem = None) -> polygon:
    item = polygon(cross_points)
    _prepare_item(item, QPen(color.darker(130), 1), color, parent)
    return item

def create_arrow(rotation_angle, color: QColor = black_color, parent: QGraphicsItem = None) -> polygon:
    item = polygon(arrow_points)
    item.setTransformOriginPoint(tile_size / 2, tile_size / 2)
    item.setRotation(rotation_angle)
    _prepare_item(item, no_pen, color, parent)
    return item

def create_circle(center: point, radius: float, color: QColor = dark_blue_color, thickness = line_width, parent: QGraphicsItem = None) -> circle:
    """
    Creates a dynamic circle of the given color and thicknes.
    """
    item = circle(center, radius)
    _prepare_item(item, QPen(color, thickness), no_color, parent)
    return item

def create_disk(center: point, radius: float, color: QColor = gray_color, parent: QGraphicsItem = None) -> circle:
    """
    Creates a dynamic filled disk of the given color.
    """
    item = circle(center, radius)
    _prepare_item(item, no_pen, color, parent)
    return item

def create_line(p1: point, p2: point, color: QColor = green_color, thickness = line_width, parent: QGraphicsItem = None) -> line:
    """
    Creates a dynamic line of the given color and thicknes.
    """
    item = line(p1, p2)
    _prepare_item(item, QPen(color, thickness), no_color, parent)
    return item

def create_rect(x: point, y: point, width: float, height: float, color: QColor = dark_gray_color, thickness = line_width, parent: QGraphicsItem = None) -> QGraphicsRectItem:
    # TODO: rectanle dynamic item, a version taking two corners.
    item = QGraphicsRectItem(0, 0, width, height)
    item.setPos(x, y)
    _prepare_item(item, QPen(black_color, thickness), color, parent)
    return item

def create_polygon(pts: List[point], color: QColor = dark_gray_color, thickness = line_width, parent: QGraphicsItem = None) -> polygon:
    """
    Create a dynamic polygon of the giuven color and line thhicknes.
    """
    item = polygon(pts)
    _prepare_item(item, QPen(color, thickness), no_color, parent)
    return item
