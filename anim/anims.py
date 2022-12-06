from anim.items.items import create_roll_circle_in_circle_angles
from .actor import actor
from .animator import animator
from .geometry import *
from .items import point, circle, item, static_point, line, polygon, rectangle
from . import trf
from .trf import pi, hpi, tau

from typing import List as _List, Callable as _Callable


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

def scaled_serie(value: float, count: int, scaler: _Callable) -> _List[float]:
    """
    Create a list containing a serie based on the given value and
    the scaler. The scaler should take a value between 0 and 1 as
    input and produce a factor to multiply the value.
    """
    fc = float(count - 1)
    return [value * scaler(i / fc) for i in range(count)]

def ondulation_serie(value: float, factor: float, count: int):
    """
    Create an ondulating series that goes from value / factor to value * factor.
    """
    log_factor = log(factor)
    def scaler(fraction: float) -> float:
        return exp(log_factor * sin(tau * fraction))
    return scaled_serie(value, count, scaler)


#################################################################
#
# Point animations

def _rotate_point_around(moved_point: point, original_pos: static_point, center: point, angle: float) -> None:
    moved_point.set_point(trf.rotate_around(original_pos, center, angle))

def rotate_point_around(moved_point: point, center: point):
    """
    Creates a function that will rotates a point around another point.
    The returned function only takes the angle in radians as parameter.
    """
    org_point = static_point(moved_point)
    return lambda angle: _rotate_point_around(moved_point, org_point, center, angle)

def _rotate_relative_point_around(moved_point: point, center: point, angle: float) -> None:
    moved_point.set_point(trf.rotate_around(moved_point.original_point, center, angle))

def rotate_relative_point_around(moved_point: point, center: point):
    """
    Creates a function that will rotates a point around another point.
    The returned function only takes the angle in radians as parameter.
    """
    return lambda angle: _rotate_relative_point_around(moved_point, center, angle)

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
# Circle animations

def change_radius(item: item):
    """
    Returns a function that sets the radius of an actor or item.
    The returned function only takes the radius.
    """
    if isinstance(item, actor):
        item = item.item
    return lambda radius: item.set_radius(radius)


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
    animator.animate_value([0., inner_center_angle], duration, rotate_relative_point_around(inner_center, outer_center))
    for pt in points_on_inner:
        animator.animate_value([0., inner_prim_angle], duration, rotate_relative_point_around(pt, point()))


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

def anim_reveal_thickness(animator: animator, duration: float, item, zoom_factor: float = 5.):
    if isinstance(item, actor):
        item = item.item
    animator.animate_value([0., 1.], duration, reveal_item(item))
    animator.animate_value(ondulation_serie(item.get_thickness(), zoom_factor, 10), duration, lambda t: item.thickness(t))

def anim_reveal_radius(animator: animator, duration: float, item, zoom_factor: float = 2.):
    if isinstance(item, actor):
        item = item.item
    animator.animate_value([0., 1.], duration, reveal_item(item))
    animator.animate_value(ondulation_serie(item.radius, zoom_factor, 10), duration, lambda r: item.set_radius(r))


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
    Returns a function that centers an item on another.
    """
    if isinstance(item, actor):
        item = item.item
    if isinstance(other, actor):
        other = other.item
    return lambda _: item.center_on(other) if item and other else None
