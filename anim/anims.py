from .actor import actor
from .animator import animator
from .items import point, circle
from . import trf

from typing import List as _List


#################################################################
#
# Float animations

def linear_serie(start: float, value: float, count: int) -> _List[float]:
    """
    Create a list containing a geometric serie starting at a given value
    with successive values increasing by the value.
    """
    return [start + value * i for i in range(count)]

def geometric_serie(start: float, value: float, ratio: float, count: int) -> _List[float]:
    """
    Create a list containing a geometric serie starting at a given value
    with successive values being in the given ratio.
    """
    return [start + value * (ratio ** i) for i in range(count)]


#################################################################
#
# Point animations

def _rotate_point_around(moved_point: point, center: point, angle: float) -> None:
    moved_point.set_point(trf.rotate_around(moved_point.original_point, center, angle))

def rotate_point_around(moved_point: point, center: point):
    """
    Creates a function that will rotates a point around another point of the given angle.
    The returned function only takes the angle in degrees as parameter.
    """
    return lambda angle: _rotate_point_around(moved_point, center, angle)

def move_point(moved_point: point):
    """
    Returns a function that animate the movement of the point to a destination point.
    The returned function only takes the position as parameter.
    """
    return lambda pt: moved_point.set_point(point(pt))


#################################################################
#
# Complex animations

def roll_circle_in_circle(animator: animator, duration: float, inner_circle: circle, outer_circle: circle, rotation_count: float, points_on_inner: _List[point]):
    # TODO: the following code assumes the points to be moved are relative to the inner circle center.
    outer_center, outer_radius = outer_circle.get_center_and_radius()
    inner_center, inner_radius = inner_circle.get_center_and_radius()
    outer_angle = 360. * rotation_count
    radius_ratio = inner_radius / outer_radius
    inner_angle = 360. * rotation_count * (1. - radius_ratio) * (1. / radius_ratio)
    animator.animate_value(0., outer_angle, duration, rotate_point_around(inner_center, outer_center))
    for pt in points_on_inner:
        animator.animate_value(0., -inner_angle, duration, rotate_point_around(pt, point()))


#################################################################
#
# Actor / item animations

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
