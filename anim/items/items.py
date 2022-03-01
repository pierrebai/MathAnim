from .circle import circle, radius_circle, diameter_circle
from .line import line
from .polygon import polygon
from .rectangle import rectangle, center_rectangle, static_rectangle
from .pointing_arrow import pointing_arrow
from .point import point, relative_point, static_point
from .text import scaling_text, fixed_size_text
from .item import item
from .pen import pen
from .color import color
from .. import trf

import math
from typing import List as _List, Tuple as _Tuple

"""
Helpers to create various kind of scene items.
"""


#################################################################
#
# Sizes

outer_size = 1000.
line_width = outer_size / 50.
dot_size = line_width * 1.5
tile_size = outer_size / 100.
half_tile_size = tile_size / 2.


#################################################################
#
# Colors

no_color = color(0, 0, 0, 0)

orange    = color(235, 180,  40, 220)
blue      = color( 68, 125, 255, 200)
green     = color( 83, 223,  56, 200)
black     = color(  0,   0,   0)
white     = color(255, 255, 255)
cyan      = color( 30, 190, 220)
gray      = color(220, 220, 220, 120)
red       = color(255,  84,  46)

dark_orange   = orange.darker(130)
dark_blue     = blue.darker(130)
dark_green    = green.darker(130)
dark_cyan     = cyan.darker(130)
dark_gray     = gray.darker(130)
dark_red      = red.darker(130)

pale_blue     = blue.lighter(130); pale_blue.setAlpha(120)


#################################################################
#
# Shapes

_cross_points = [
        point(-half_tile_size + 1, -half_tile_size + 3), point(-half_tile_size + 3, -half_tile_size + 1), point(0, -half_tile_size + 3),
        point( half_tile_size - 3, -half_tile_size + 1), point( half_tile_size - 1, -half_tile_size + 3), point( half_tile_size - 3, 0),
        point( half_tile_size - 1,  half_tile_size - 3), point( half_tile_size - 3,  half_tile_size - 1), point(0,  half_tile_size - 3),
        point(-half_tile_size + 3,  half_tile_size - 1), point(-half_tile_size + 1,  half_tile_size - 3), point(-half_tile_size + 3, 0),
]

_arrow_points = [
    point(-half_tile_size + 2, -half_tile_size + 5), point(0, -half_tile_size + 1),
    point( half_tile_size - 2, -half_tile_size + 5),
    point( 1, -half_tile_size + 4), point( 1,  half_tile_size - 1),
    point(-1,  half_tile_size - 1), point(-1, -half_tile_size + 4), 
]

def create_cross(origin: point, fill_color: color = red) -> polygon:
    poly_points = [relative_point(origin, pt) for pt in _cross_points]
    return polygon(poly_points).outline(fill_color.darker(130)).thickness(1).fill(fill_color)

def create_arrow(origin: point, rotation_angle, fill_color: color = black) -> polygon:
    poly_points = [relative_point(origin, trf.rotate_around_origin(pt, rotation_angle)) for pt in _arrow_points]
    return polygon(poly_points).outline(no_color).fill(fill_color)

def create_pointing_arrow(tail: point, head: point, fill_color: color = pale_blue) -> line:
    """
    Creates a dynamic pointing arrow of the given color.
    """
    return pointing_arrow(tail, head).outline(no_color).fill(fill_color)


#################################################################
#
# Points Series


#################################################################
#
# Simple Geometries

def create_circle(center: point, radius: float) -> circle:
    """
    Creates a dynamic dark blue circle.
    """
    return circle(center, radius).outline(dark_blue).thickness(line_width)

def create_disk(center: point, radius: float) -> circle:
    """
    Creates a dynamic gray filled disk.
    """
    return circle(center, radius).outline(no_color).fill(gray)

def create_line(p1: point, p2: point) -> line:
    """
    Creates a dynamic green line.
    """
    return line(p1, p2).outline(green).thickness(line_width)

def create_rect(x: float, y: float, width: float, height: float) -> rectangle:
    """
    Creates a gray rectangle outlined in black.
    """
    return rectangle(point(x, y), point(x+width, y+height)).outline(black).thickness(line_width).fill(dark_gray)

def create_invisible_rect(x: float, y: float, width: float, height: float) -> rectangle:
    return rectangle(point(x, y), point(x+width, y+height)).fill(no_color).outline(no_color).thickness(0).set_opacity(0.)

def create_two_points_rect(p1: point, p2: point) -> rectangle:
    """
    Creates a dynamic dark gray rectangle out of two corners outlined in black.
    """
    return rectangle(p1, p2).outline(black).thickness(line_width).fill(dark_gray)

def create_center_rect(p1: point, width: float, height: float) -> rectangle:
    """
    Creates a dynamic dark gray rectangle out of its center position and width and height, outlined in black.
    """
    return center_rectangle(p1, width, height).outline(black).thickness(line_width).fill(dark_gray)

def create_losange(base_point: point, height: float) -> polygon:
    """
    Create a losange standing on the base point.
    All points are relative to the given base.
    """
    return create_polygon([
        relative_point(base_point,           0.,  0.),
        relative_point(base_point, -height / 2., -height / 2.),
        relative_point(base_point,           0., -height),
        relative_point(base_point,  height / 2., -height / 2.),
    ]).outline(no_color).thickness(0)


#################################################################
#
# Polygons

def create_multi_polygons(lists_of_points: _List[_List[point]]) -> _List[polygon]:
    """
    Creates multiple polygons from a list of lists of points.
    """
    return [create_polygon(points) for points in lists_of_points]


def create_polygon(pts: _List[point]) -> polygon:
    """
    Create a dynamic polygo, outlined in dark gray.
    """
    return polygon(pts).outline(dark_gray).thickness(line_width)

#################################################################
#
# Points distributions

def create_roll_circle_in_circle_points(inner_radius: float, outer_radius: float, rotation_count: float, point_count: int, inner_radius_ratio = 1.) -> _List[point]:
    center_angle, perim_angle = create_roll_circle_in_circle_angles(inner_radius, outer_radius, rotation_count)
    center_angles = [center_angle * i / point_count for i in range(point_count)]
    perim_angles  = [perim_angle  * i / point_count for i in range(point_count)]
    inner_center = static_point(outer_radius - inner_radius, 0.)
    dot = static_point(inner_radius * inner_radius_ratio, 0.)
    return [relative_point(
        point(trf.rotate_around_origin(inner_center, center_angle)),
        trf.rotate_around_origin(dot, perim_angle))
        for center_angle, perim_angle in zip(center_angles, perim_angles)]

def create_roll_circle_in_circle_angles(inner_radius: float, outer_radius: float, rotation_count: float) -> _Tuple[float, float]:
    """
    Calculates and returns the inner circle center rotation angle
    and inner circle perimeter rotation angle as if an inner circle
    were rotating inside the outer circle.
    """
    inner_center_angle = 360. * rotation_count
    radius_ratio = inner_radius / outer_radius
    inner_perim_angle = -360. * rotation_count * (1. - radius_ratio) * (1. / radius_ratio)
    return inner_center_angle, inner_perim_angle

def create_relative_points_around_circle(circle: circle, count: int, angle_offset: float = 0.) -> _List[point]:
    """
    Creates points relative to a circle center around a circle starting at the offset angle.
    """
    center, radius = circle.get_center_and_radius()
    return create_relative_points_around_center(center, radius, count, angle_offset)

def create_relative_points_around_center(center: point, radius: float, count: int, angle_offset: float = 0.) -> _List[point]:
    """
    Creates points relative to a circle center around a circle starting at the offset angle.
    """
    deltas = create_points_around_origin(radius, count, angle_offset)
    return [relative_point(center, delta) for delta in deltas]

def create_points_around_origin(radius: float, count: int, angle_offset: float = 0.) -> _List[point]:
    """
    Creates points around the origin at a given radius starting at the offset angle.
    """
    angles = create_angles_around_origin(count, angle_offset)
    return [point(math.cos(angle) * radius, math.sin(angle) * radius) for angle in angles]

def create_angles_around_origin(count: int, angle_offset: float = 0.) -> _List[float]:
    """
    Distribute angles around a circle starting at the offset angle.
    """
    return [angle_offset + math.pi * 2. * i / count for i in range(count)]

def create_circles_on_centers(centers: _List[point], radius: float) -> _List[circle]:
    """
    Creates circles of a same radius on all given centers.
    """
    return [circle(center, radius) for center in centers]

def transpose_lists(list_of_lists: _List[list]) -> _List[list]:
    """
    Creates a list of lists by assembling every ith elements of the input lists together in the ith output list.
    This assumes all input lists contain the same number of elements.
    """
    if not list_of_lists:
        return []
    outer_count = len(list_of_lists)
    inner_count = len(list_of_lists[0])
    return [[list_of_lists[outer][inner] for outer in range(outer_count)] for inner in range(inner_count)]
    

#################################################################
#
# Text

def create_scaling_sans_text(label: str, pt: point, font_size: float) -> scaling_text:
    new_text = scaling_text(label, pt)
    new_text.set_sans_font(font_size)
    return new_text

def create_equation(equation: str, pt: point, font_size: float) -> _List[scaling_text]:
    parts = equation.split()
    if not parts:
        return []

    texts: _List[scaling_text] = []

    def create_eq_text(pt: point, part: str, font_size: float, as_exponent = False) -> relative_point:
        nonlocal texts
        if as_exponent:
            pt = texts[-1].exponent_pos()
            font_size /= 2
        elif len(texts):
            part = ' ' + part
        texts.append(create_scaling_sans_text(part, pt, font_size))
        return relative_point(pt, texts[-1].scene_rect().width(), 0.)

    pt = create_eq_text(pt, parts[0], font_size)

    next_as_exponent = False
    for part in parts[1:]:
        if part == '^':
            next_as_exponent = True
            continue
        pt = create_eq_text(pt, part, font_size, next_as_exponent)
        next_as_exponent = False

    return texts
