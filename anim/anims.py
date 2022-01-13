from PyQt5.QtGui import QTransform
from .actor import actor
from .items import point
from . import trf

##########################################
# Point animations.

def _rotate_point_around(point: point, center: point, angle: float):
    point.set_point(trf.rotate_around(point.original_point, center, angle))

def rotate_point_around(point: point, center: point):
    return lambda angle: _rotate_point_around(point, center, angle)


##########################################
# Actor / item animations.

def reveal_item(item):
    """
    Returns a function that animate the opacity of the actor or item.
    """
    if isinstance(item, actor):
        item = item.item
    return lambda opacity: item.setOpacity(opacity)

def rotate_item(item):
    """
    Returns a function that animate the rotation of the actor or item aorund its own center.
    """
    if isinstance(item, actor):
        item = item.item
    return lambda angle: item.setRotation(angle)
