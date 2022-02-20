from .actor import actor
from .items import point, static_point
from . import trf

from typing import List


##########################################
# Float animations.

def linear_serie(start: float, value: float, count: int) -> List[float]:
    """
    Create a list containing a geometric serie starting at a given value
    with successive values increasing by the value.
    """
    return [start + value * i for i in range(count)]

def geometric_serie(start: float, value: float, ratio: float, count: int) -> List[float]:
    """
    Create a list containing a geometric serie starting at a given value
    with successive values being in the given ratio.
    """
    return [start + value * (ratio ** i) for i in range(count)]


##########################################
# Point animations.

def _rotate_point_around(point: point, center: point, angle: float) -> None:
    point.set_point(trf.rotate_around(point.original_point, center, angle))

def rotate_point_around(point: point, center: point):
    """
    Creates a function that will rotates a point around another point of the given angle.
    The returned function only takes the angle in degrees as parameter.
    """
    return lambda angle: _rotate_point_around(point, center, angle)

def move_point(point: point):
    """
    Returns a function that animate the movement of the point to a destination point.
    The returned function only takes the position as parameter.
    """
    return lambda pt: point.set_point(static_point(pt.x(), pt.y()))


##########################################
# Actor / item animations.

def reveal_item(item):
    """
    Returns a function that animate the opacity of the actor or item.
    The returned function only takes the opacity as parameter, from 0 to 1.
    """
    if isinstance(item, actor):
        item = item.item
    return lambda opacity: item.set_opacity(opacity) if item else None

def _scale_text_item(item, size) -> None:
    item.set_font(item.get_font_name(), max(0.5, size))

def scale_text_item(item):
    """
    Returns a function that animate the font size of the actor or item.
    The returned function only takes the font size as parameter.
    """
    if isinstance(item, actor):
        item = item.item
    return lambda size: _scale_text_item(item, size) if item else None
