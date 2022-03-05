from .items.line import line
from .items.point import point, static_point

import math
from typing import List as _List, Tuple as _Tuple


#################################################################
#
# Centers

def center_of(points: _List[static_point]) -> static_point:
    total = static_point()
    for pt in points:
        total = total + pt
    return total / len(points)


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
    d1 = two_points_distance(l1_p1, l1_p2)
    d2 = two_points_distance(l2_p1, l2_p2)
    d = min(d1, d2)
    p2 = point(p1 + static_point(math.cos(bisector_angle) * d, math.sin(bisector_angle) * d))
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
    Returns the angle between the X axis and the line formed by the two points.
    """
    delta = p2 - p1
    return math.atan2(delta.y(), delta.x())


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

def two_points_distance(p1: static_point, p2: static_point) -> float:
    """
    Returns the distance between two points.
    """
    return delta_distance(p2 - p1)

def delta_distance(delta: static_point) -> float:
    """
    Returns the length of the delta.
    """
    return math.sqrt(delta.x() ** 2 + delta.y() ** 2)

def point_to_line_distance(pt: static_point, line: line) -> float:
    return point_to_two_points_distance(pt, line.p1, line.p2)

def point_to_two_points_distance(pt: static_point, p1: static_point, p2: static_point) -> float:
    delta = p2 - p1
    delta_dot = two_points_dot(delta, delta)
    if not delta_dot:
        return two_points_distance(pt, p1)
    t = two_points_dot(pt - p1, delta) / delta_dot
    if -epsilon < t < 1. + epsilon:
        ox = p1.x() + t * (p2.x() - p1.x())
        oy = p1.y() + t * (p2.y() - p1.y())
        return math.sqrt((pt.x() - ox) ** 2 + (pt.y() - oy) ** 2)
    elif t < 0.:
        return two_points_distance(pt, p1)
    else:
        return two_points_distance(pt, p2)


#################################################################
#
# Projections

def two_points_convex_sum(p1: static_point, p2: static_point, t: float) -> point:
    return point(p1 * (1. - t) + p2 * t)

def point_to_line_projection(pt: static_point, line: line) -> point:
    return point_to_two_points_projection(pt, line.p1, line.p2)

def point_to_two_points_projection(pt: static_point, p1: static_point, p2: static_point) -> point:
    delta = p2 - p1
    delta_dot = two_points_dot(delta, delta)
    if not delta_dot:
        return p1
    t = two_points_dot(pt - p1, delta) / delta_dot
    return two_points_convex_sum(p1 , p2, t)


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
