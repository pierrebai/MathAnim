from .items.line import line
from .items.point import point, static_point

from math import cos, sin, atan2, sqrt, pi, exp, log
from typing import List as _List, Tuple as _Tuple

hpi = pi / 2.
qpi = pi / 4.
tau = pi * 2.
origin = point(0., 0.)

#################################################################
#
# Min/max

def min_max(points: _List[static_point]) -> _Tuple[static_point]:
    minX = min([pt.x() for pt in points])
    maxX = max([pt.x() for pt in points])
    minY = min([pt.y() for pt in points])
    maxY = max([pt.y() for pt in points])
    return static_point(minX, minY), static_point(maxX, maxY)


#################################################################
#
# Centers

def weighted_center_of(points: _List[static_point]) -> static_point:
    total = static_point()
    for pt in points:
        total = total + pt
    return total / len(points)

def center_of(points: _List[static_point]) -> static_point:
    p1, p2 = min_max(points)
    return (p1 + p2) / 2.


#################################################################
#
# Bisectors

def two_lines_bisector(l1: line, l2: line) -> line:
    return line(*four_points_bisector(l1.p1, l1.p2, l2.p1, l2.p2))

def four_points_bisector(l1_p1: static_point, l1_p2: static_point, l2_p1: static_point, l2_p2: static_point) -> _Tuple[point, point]:
    p1 = four_points_any_intersection(l1_p1, l1_p2, l2_p1, l2_p2)
    if p1 is None:
        return (point((l1_p1 + l2_p1) / 2.), point((l1_p2 + l2_p2) / 2.))
    a1 = two_points_angle(l1_p1, l1_p2)
    a2 = two_points_angle(l2_p1, l2_p2)
    bisector_angle = (a1 + a2) / 2.
    d1 = point.distance(l1_p1, l1_p2)
    d2 = point.distance(l2_p1, l2_p2)
    d = min(d1, d2)
    p2 = point(p1 + static_point(cos(bisector_angle) * d, sin(bisector_angle) * d))
    return (p1, p2)


#################################################################
#
# Angles

def two_lines_angle(l1: line, l2: line) -> float:
    """
    Returns the angle between the lines.
    """
    return line_angle(l2) - line_angle(l1)

def line_angle(line: line) -> float:
    """
    Returns the angle between the X axis and the line.
    """
    return two_points_angle(line.p1, line.p2)

def four_points_angle(l1_p1: static_point, l1_p2: static_point, l2_p1: static_point, l2_p2: static_point) -> float:
    """
    Returns the angle between the lines formed by the four points.
    """
    return two_points_angle(l2_p1, l2_p2) - two_points_angle(l1_p1, l1_p2)

def two_points_angle(p1: static_point, p2: static_point) -> float:
    """
    Returns the angle in degrees between the X axis and the line formed by the two points.
    """
    delta = p2 - p1
    return atan2(delta.y(), delta.x())

#################################################################
#
# Angles to align lines

def straighten_angle(p1: point, p2: point, horizontal) -> float:
    """
    Returns the angle by which the points must be rotated
    to aligned the line to be horizontal or vertical.
    """
    extra = 0. if horizontal else hpi
    angle = -two_points_angle(p1, p2) + extra
    if angle >= pi:
        angle -= pi
    if angle <= -pi:
        angle += pi
    return angle

def horizontal_angle(p1: point, p2: point) -> float:
    """
    Returns the angle by which the points must be rotated
    to aligned the line to be horizontal.
    """
    return straighten_angle(p1, p2, True)

def vertical_angle(p1: point, p2: point) -> float:
    """
    Returns the angle by which the points must be rotated
    to aligned the line to be vertical.
    """
    return straighten_angle(p1, p2, False)


#################################################################
#
# Dot products.

def two_points_dot(p1: static_point, p2: static_point) -> float:
    return p1.x() * p2.x() + p1.y() * p2.y()

def two_points_sin_dot(p1: static_point, p2: static_point) -> float:
    return p1.y() * p2.x() - p1.x() * p2.y()


#################################################################
#
# Distances

def point_to_line_distance(pt: static_point, line: line) -> float:
    return point_to_two_points_distance(pt, line.p1, line.p2)

def point_to_two_points_distance(pt: static_point, p1: static_point, p2: static_point) -> float:
    delta = p2 - p1
    delta_dot = two_points_dot(delta, delta)
    if not delta_dot:
        return point.distance(pt, p1)
    t = two_points_dot(pt - p1, delta) / delta_dot
    if -epsilon < t < 1. + epsilon:
        ox = p1.x() + t * (p2.x() - p1.x())
        oy = p1.y() + t * (p2.y() - p1.y())
        return sqrt((pt.x() - ox) ** 2 + (pt.y() - oy) ** 2)
    elif t < 0.:
        return point.distance(pt, p1)
    else:
        return point.distance(pt, p2)


#################################################################
#
# Projections

def two_points_convex_sum(p1: static_point, p2: static_point, t: float) -> point:
    return point(p1 * (1. - t) + p2 * t)

def mid_point(p1: static_point, p2: static_point) -> point:
    return two_points_convex_sum(p1, p2, 0.5)

def point_to_line_projection(pt: static_point, line: line) -> point:
    return point_to_two_points_projection(pt, line.p1, line.p2)

def point_to_two_points_projection(pt: static_point, p1: static_point, p2: static_point) -> point:
    delta = p2 - p1
    delta_dot = two_points_dot(delta, delta)
    if not delta_dot:
        return p1
    t = two_points_dot(pt - p1, delta) / delta_dot
    return two_points_convex_sum(p1 , p2, t)

def mirror_point_on_line(mirrored_point: point, mirror_line: line, ratio: float = 1.) -> static_point:
    # The following is equivalent to these steps, but with each equation
    # folded into the next:
    #
    #     delta = org_point - pt_on_line
    #     mirror = pt_on_line - delta
    #     delta = org_point - mirror
    #     position = org_point - delta * ratio
    #     mirrored_point.set_absolute_point(position)
    pt_on_line = point_to_line_projection(mirrored_point, mirror_line)
    return mirrored_point - (mirrored_point - pt_on_line) * (2 * ratio)


#################################################################
#
# Intersections

epsilon = 0.00001

def two_lines_intersection(l1: line, l2: line) -> point:
    """
    Returns the intersection point of two lines.
    Returns None if parallel or if it ends up outside of the lines.
    """
    return four_points_intersection(l1.p1, l1.p2, l2.p1, l2.p2)

def two_lines_any_intersection(l1: line, l2: line) -> point:
    """
    Returns the intersection point of two lines, even if outside the lines.
    Returns None if parallel.
    """
    return four_points_any_intersection(l1.p1, l1.p2, l2.p1, l2.p2)

def two_lines_intersection_within(l1: line, l2: line) -> point:
    """
    Returns the intersection point of two lines, but not if on end-points.
    Returns None if parallel.
    """
    return four_points_intersection_within(l1.p1, l1.p2, l2.p1, l2.p2)

def four_points_intersection(l1_p1: static_point, l1_p2: static_point, l2_p1: static_point, l2_p2: static_point) -> point:
    """
    Returns the intersection point of the two lines formed by the four points.
    Returns None if parallel or if it ends up outside of the lines.
    """
    params = _stay_on_units(_interesection_params(l1_p1, l1_p2, l2_p1, l2_p2))
    if params is None:
        return params
    return two_points_convex_sum(l1_p1 , l1_p2, params.x())


def four_points_any_intersection(l1_p1: static_point, l1_p2: static_point, l2_p1: static_point, l2_p2: static_point) -> point:
    """
    Returns the intersection point of the two lines formed by the four points, even if outside the lines.
    Returns None if parallel.
    """
    params = _interesection_params(l1_p1, l1_p2, l2_p1, l2_p2)
    if params is None:
        return params
    return two_points_convex_sum(l1_p1 , l1_p2, params.x())

def four_points_intersection_within(l1_p1: static_point, l1_p2: static_point, l2_p1: static_point, l2_p2: static_point) -> point:
    """
    Returns the intersection point of the two lines formed by the four points, but not if on end-points.
    Returns None if parallel.
    """
    params = _stay_on_units(_interesection_params(l1_p1, l1_p2, l2_p1, l2_p2))
    if params is None:
        return params
    px = params.x()
    py = params.y()
    if px < epsilon or px > (1. - epsilon) or py < epsilon or py > (1. - epsilon):
        return None
    return two_points_convex_sum(l1_p1 , l1_p2, px)

def _interesection_params(l1_p1: static_point, l1_p2: static_point, l2_p1: static_point, l2_p2: static_point) -> static_point:
    l1_p1_x = l1_p1.x(); l1_p1_y = l1_p1.y()
    l1_p2_x = l1_p2.x(); l1_p2_y = l1_p2.y()
    l2_p1_x = l2_p1.x(); l2_p1_y = l2_p1.y()
    l2_p2_x = l2_p2.x(); l2_p2_y = l2_p2.y()

    l1_dx = l1_p2_x - l1_p1_x; l1_dy = l1_p2_y - l1_p1_y
    l2_dx = l2_p2_x - l2_p1_x; l2_dy = l2_p2_y - l2_p1_y

    # Check parallel
    det = (l1_dx * l2_dy) - (l1_dy * l2_dx)
    if -epsilon < det < epsilon:
        return None

    l1_param = -((l1_p1_x * l2_dy) + l2_p1_x * (l1_p1_y - l2_p2_y) + l2_p2_x * (l2_p1_y - l1_p1_y)) / det
    l2_param =  ((l1_p1_x * (l2_p1_y - l1_p2_y)) + l1_p2_x * (l1_p1_y - l2_p1_y) + l2_p1_x * l1_dy) / det

    return static_point(l1_param, l2_param)

def _stay_on_units(params: static_point) -> static_point:
    """
    Coerce the params to be invalid if not both in the range [0., 1.].
    """
    l1_param = params.x()
    if l1_param < -epsilon or l1_param > 1.0 + epsilon:
        return None

    l2_param = params.y()
    if l2_param < -epsilon or l2_param > 1.0 + epsilon:
        return None

    return params


#################################################################
#
# Points spreads

def create_triangle_rows_of_count(rows: int) -> _List[int]:
    """
    Creates a list of counts of each row of a triangle of things.
    """
    return [count for count in range(1, rows+1)]

def create_triangle_rows_of_numbers(rows: int, start = 0) -> _List[int]:
    """
    Creates a triangle of rows of numbers.
    """
    rows_of_count = create_triangle_rows_of_count(rows)
    rows_of_nmumbers = []
    for count in rows_of_count:
        rows_of_nmumbers.append([i + start for i in range(count)])
        start += count+1
    return rows_of_nmumbers

def create_rows_of_points(rows_of_count: _List[int], top: point, element_size: static_point, row_offset: static_point) -> _List[_List[point]]:
    """
    Creates a list of lists of points in an arrangement of rows starting at top.
    Each row is offset from the preceeding by the row_offset. (Both the vertical and horizontal offsets.)
    Each element in the triangle has the given element size.
    """
    pos = static_point(top)
    width = element_size.x()
    rows_of_points = []
    for count in rows_of_count:
        row = [point(pos + static_point(col * 2. * width, 0)) for col in range(count)]
        rows_of_points.append(row)
        pos = pos + row_offset
    return rows_of_points

def create_triangle_of_points(rows: int, top: point, element_size: static_point) -> _List[_List[point]]:
    """
    Creates a list of points in a triagular arrangement starting at top.
    Each element in the triangle has the given element size.
    """
    return create_rows_of_points(
        create_triangle_rows_of_count(rows), top, element_size, static_point(-element_size.x(), element_size.y()))
