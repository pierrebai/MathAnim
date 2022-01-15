from .actor import actor
from . import point
from . import trf

from PySide6.QtCore import QPointF

##########################################
# Point animations.

def _rotate_point_around(point: point, center: point, angle: float):
    point.set_point(trf.rotate_around(point.original_point, center, angle))

def rotate_point_around(point: point, center: point):
    """
    Creates a function that will rotates a point around another point of the given angle.
    The returned function only takes the angle in degrees as parameter.
    """
    return lambda angle: _rotate_point_around(point, center, angle)


##########################################
# Actor / item animations.

def reveal_item(item):
    """
    Returns a function that animate the opacity of the actor or item.
    The returned function only takes the opacity as parameter, from 0 to 1.
    """
    if isinstance(item, actor):
        item = item.item
    return lambda opacity: item.setOpacity(opacity) if item else None

def rotate_item(item):
    """
    Returns a function that animate the rotation of the actor or item around its own center.
    The returned function only takes the angle in degrees as parameter.
    """
    if isinstance(item, actor):
        item = item.item
    return lambda angle: item.setRotation(angle) if item else None

def move_item(item):
    """
    Returns a function that animate the rotation of the actor or item around its own center.
    The returned function only takes the angle in degrees as parameter.
    """
    if isinstance(item, actor):
        item = item.item
    return lambda pt: item.setPos(pt) if item else None
