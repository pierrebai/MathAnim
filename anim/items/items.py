from .circle import circle, radius_circle, diameter_circle
from .line import line
from .polygon import polygon
from .rectangle import rectangle, center_rectangle
from .pointing_arrow import pointing_arrow
from .point import point, relative_point, static_point
from .text import scaling_text, fixed_size_text
from .item import item
from .pen import pen
from .color import color
from .. import trf

from typing import List as _List

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

orange_color    = color(235, 180,  40, 220)
blue_color      = color( 68, 125, 255, 200)
green_color     = color( 83, 223,  56, 200)
black_color     = color(  0,   0,   0)
white_color     = color(255, 255, 255)
cyan_color      = color( 30, 190, 220)
gray_color      = color(220, 220, 220, 120)
red_color       = color(255,  84,  46)

dark_orange_color   = orange_color.darker(130)
dark_blue_color     = blue_color.darker(130)
dark_green_color    = green_color.darker(130)
dark_cyan_color     = cyan_color.darker(130)
dark_gray_color     = gray_color.darker(130)
dark_red_color      = red_color.darker(130)

pale_blue_color     = blue_color.lighter(130); pale_blue_color.setAlpha(120)

no_pen   = pen(no_color, 0)


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

def _prepare_item(item: item, outline_color: color, thickness:float, fill_color: color) -> None:
    item.outline(outline_color).thickness(thickness).fill(fill_color)

def create_cross(origin: point, fill_color: color = red_color) -> polygon:
    poly_points = [relative_point(origin, pt) for pt in _cross_points]
    item = polygon(poly_points)
    _prepare_item(item, fill_color.darker(130), 1., fill_color)
    return item

def create_arrow(origin: point, rotation_angle, fill_color: color = black_color) -> polygon:
    poly_points = [relative_point(origin, trf.rotate_around_origin(pt, rotation_angle)) for pt in _arrow_points]
    item = polygon(poly_points)
    _prepare_item(item, no_color, 0., fill_color)
    return item

def create_pointing_arrow(tail: point, head: point, fill_color: color = pale_blue_color) -> line:
    """
    Creates a dynamic pointing arrow of the given color.
    """
    item = pointing_arrow(tail, head)
    _prepare_item(item, no_color, 0, fill_color)
    return item


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
    item = circle(center, radius)
    _prepare_item(item, dark_blue_color, line_width, no_color)
    return item

def create_disk(center: point, radius: float) -> circle:
    """
    Creates a dynamic gray filled disk.
    """
    item = circle(center, radius)
    _prepare_item(item, no_color, 0., gray_color)
    return item

def create_line(p1: point, p2: point) -> line:
    """
    Creates a dynamic green line.
    """
    item = line(p1, p2)
    item.outline(green_color).thickness(line_width)
    return item

def create_rect(x: float, y: float, width: float, height: float) -> rectangle:
    """
    Creates a gray rectangle outlined in black.
    """
    item = rectangle(point(x, y), point(x+width, y+height))
    _prepare_item(item, black_color, line_width, dark_gray_color)
    return item

def create_invisible_rect(x: float, y: float, width: float, height: float) -> rectangle:
    item = create_rect(x, y, width, height).fill(no_color).outline(no_color).thickness(0)
    item.set_opacity(0.)
    return item

def create_two_points_rect(p1: point, p2: point) -> rectangle:
    """
    Creates a dynamic dark gray rectangle out of two corners outlined in black.
    """
    item = rectangle(p1, p2)
    _prepare_item(item, black_color, line_width, dark_gray_color)
    return item

def create_center_rect(p1: point, width: float, height: float) -> rectangle:
    """
    Creates a dynamic dark gray rectangle out of its center position and width and height, outlined in black.
    """
    item = center_rectangle(p1, width, height)
    _prepare_item(item, black_color, line_width, dark_gray_color)
    return item

def create_polygon(pts: _List[point]) -> polygon:
    """
    Create a dynamic polygo, outlined in dark gray.
    """
    item = polygon(pts)
    _prepare_item(item, dark_gray_color, line_width, no_color)
    return item

def create_losange(base_point: point, height: float) -> polygon:
    """
    Create a losange standing on the base point.
    All points are relative to the given base.
    """
    return create_polygon([
        relative_point(base_point,         0.,  0.),
        relative_point(base_point, -height / 2., -height / 2.),
        relative_point(base_point,         0., -height),
        relative_point(base_point,  height / 2., -height / 2.),
    ]).outline(no_color).thickness(0)


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
