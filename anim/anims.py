from anim.items.items import create_roll_circle_in_circle_angles
from .actor import actor
from .animator import animator
from .items import point, circle, item, static_point
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

def _rotate_point_around(moved_point: point, original_pos: static_point, center: point, angle: float) -> None:
    moved_point.set_point(trf.rotate_around(original_pos, center, angle))

def rotate_point_around(moved_point: point, center: point):
    """
    Creates a function that will rotates a point around another point.
    The returned function only takes the angle in degrees as parameter.
    """
    org_point = static_point(moved_point)
    return lambda angle: _rotate_point_around(moved_point, org_point, center, angle)

def move_point(moved_point: point):
    """
    Returns a function that sets the position of the point.
    The returned function only takes the position as parameter.
    """
    return lambda pt: moved_point.set_point(point(pt))


#################################################################
#
# Color animations

def change_fill_color(item: item):
    """
    Returns a function that sets the fill color of an actor or item.
    The returned function only takes the color.
    """
    if isinstance(item, actor):
        item = item.item
    return lambda co: item.fill(co)


#################################################################
#
# Complex animations

def roll_points_on_circle_in_circle(animator: animator, duration: float, inner_circle: circle, outer_circle: circle, rotation_count: float, points_on_inner: _List[point]):
    """
    Animate relative points that are relative to an inner circle center
    as if the inner circle were rotating in the outer circle.
    """
    inner_center, inner_radius = inner_circle.get_center_and_radius()
    outer_center, outer_radius = outer_circle.get_center_and_radius()
    inner_center_angle, inner_prim_angle = create_roll_circle_in_circle_angles(inner_radius, outer_radius, rotation_count)
    animator.animate_value([0., inner_center_angle], duration, rotate_point_around(inner_center, outer_center))
    for pt in points_on_inner:
        animator.animate_value([0., inner_prim_angle], duration, rotate_point_around(pt, point()))


#################################################################
#
# Actor / item animations

def reveal_item(item):
    """
    Returns a function that sets the opacity of the actor or item.
    The returned function only takes the opacity as parameter, from 0 to 1.
    """
    if isinstance(item, actor):
        item = item.item
    return lambda opacity: item.set_opacity(opacity) if item else None


#################################################################
#
# Text animations

def _scale_text_item(item, size) -> None:
    item.set_font(item.get_font_name(), max(0.5, size))

def scale_text_item(item):
    """
    Returns a function that sets the font size of the actor or item.
    The returned function only takes the font size as parameter.
    """
    if isinstance(item, actor):
        item = item.item
    return lambda size: _scale_text_item(item, size) if item else None

def center_text_item_on(item, other):
    """
    Returns a function that sets the font size of the actor or item.
    The returned function only takes the font size as parameter.
    """
    if isinstance(item, actor):
        item = item.item
    if isinstance(other, actor):
        other = other.item
    return lambda _: item.center_on(other) if item and other else None
