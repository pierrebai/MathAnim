from anim.items.items import create_roll_circle_in_circle_angles
from .actor import actor
from .animator import animator
from .geometry import *
from .geometries import geometries
from .maths import ondulation_serie
from .points import points
from .items import point, circle, item, static_point, line, polygon, rectangle, scaling_text
from . import trf

from typing import List as _List, Callable as _Callable


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

def _rotate_absolute_point_around(moved_point: point, original_pos: static_point, center: point, angle: float) -> None:
    moved_point.set_absolute_point(trf.rotate_around(original_pos, center, angle))

def rotate_absolute_point_around(moved_point: point, center: point):
    """
    Creates a function that will rotates a point around another point
    by setting its absolute position.
    The returned function only takes the angle in radians as parameter.
    """
    org_point = static_point(moved_point)
    return lambda angle: _rotate_absolute_point_around(moved_point, org_point, center, angle)

def _rotate_relative_point_around(moved_point: point, center: point, angle: float) -> None:
    moved_point.set_point(trf.rotate_around(moved_point.original_delta, center, angle))

def rotate_relative_point_around(moved_point: point, center: point):
    """
    Creates a function that will rotates a point around another point.
    The returned function only takes the angle in radians as parameter.
    """
    return lambda angle: _rotate_relative_point_around(moved_point, center, angle)

def move_point(moved_point: point):
    """
    Returns a function that sets the position of the point.
    For relative points, that changes the delta, not the position.
    The returned function only takes the position as parameter.
    """
    return lambda pt: moved_point.set_point(point(pt)) if pt else None

def move_absolute_point(moved_point: point):
    """
    Returns a function that sets the absolute position of the point.
    The returned function only takes the position as parameter.
    """
    return lambda pt: moved_point.set_absolute_point(point(pt)) if pt else None

def move_point_to_line_mirror(mirrored_point: point, mirror_line: line):
    """
    Returns a function that mirrors the position of the point
    around the given line.
    The retiurned function only takes the ratio between zero
    and one of the complete mirror.
    """
    org_point = static_point(mirrored_point)
    return lambda ratio: mirrored_point.set_absolute_point(mirror_point_on_line(org_point, mirror_line, ratio))


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
    return lambda co: item.fill(co) if item else None


#################################################################
#
# Items animations

def change_radius(item: item):
    """
    Returns a function that sets the radius of an actor or item.
    The returned function only takes the radius.
    """
    if isinstance(item, actor):
        item = item.item
    return lambda radius: item.set_radius(radius) if item else None

def change_thickness(item: item):
    """
    Returns a function that sets the thickness of an actor or item.
    The returned function only takes the thickness.
    """
    if isinstance(item, actor):
        item = item.item
    return lambda thickness: item.thickness(thickness) if item else None


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

def anim_reveal_item(animator: animator, duration: float, item):
    """
    Adds an animation to reveal the item in the given duration.
    """
    animator.animate_value([0., 1., 1.], duration, reveal_item(item))

def anim_hide_item(animator: animator, duration: float, item):
    """
    Adds an animation to hide the item in the given duration.
    """
    animator.animate_value([1., 0.], duration, reveal_item(item))

def anim_reveal_thickness(animator: animator, duration: float, item, zoom_factor: float = 5.):
    """
    Adds an animation to reveal the item and ondulate its thickness in the given duration.
    """
    if isinstance(item, actor):
        item = item.item
    animator.animate_value([0., 1., 1.], duration, reveal_item(item))
    animator.animate_value(ondulation_serie(item.get_thickness(), zoom_factor, 10), duration, change_thickness(item))

def anim_ondulate_radius(animator: animator, duration: float, item, zoom_factor: float = 2.):
    """
    Adds an animation to ondulate the radius of an item in the given duration.
    """
    if isinstance(item, actor):
        item = item.item
    animator.animate_value(ondulation_serie(item.radius, zoom_factor, 10), duration, change_radius(item))

def anim_reveal_radius(animator: animator, duration: float, item, zoom_factor: float = 2.):
    if isinstance(item, actor):
        item = item.item
    animator.animate_value([0., 1.], duration / 3., reveal_item(item))
    anim_ondulate_radius(animator, duration, item, zoom_factor)


#################################################################
#
# Text animations

def _scale_text_item(item: scaling_text, size: float) -> None:
    item.set_font(item.get_font_name(), max(0.5, size), item.font().bold())

def scale_text_item(item: scaling_text):
    """
    Returns a function that sets the font size of the actor or item.
    The returned function only takes the font size as parameter.
    """
    if isinstance(item, actor):
        item = item.item
    return lambda size: _scale_text_item(item, size) if item else None

def anim_ondulate_text_size(animator: animator, duration: float, item: scaling_text, zoom_factor: float = 2.):
    """
    Adds an animation to ondulate a text item size for the given duration.
    """
    if isinstance(item, actor):
        item = item.item
    animator.animate_value(ondulation_serie(item.get_font_size(), zoom_factor, 10), duration, scale_text_item(item))

def center_text_item_on(item, other):
    """
    Returns a function that centers an item on another.
    """
    if isinstance(item, actor):
        item = item.item
    if isinstance(other, actor):
        other = other.item
    return lambda _: item.center_on(other) if item and other else None
