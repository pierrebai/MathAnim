import anim
import math

from typing import List, Tuple

#################################################################
#
# Description

name = "Vortex Maths"
description = "Mathologer video https://www.youtube.com/watch?v=6ZrO90AI0c8&t=7s"
loop = False
reset_on_change = True


#################################################################
#
# Options

number_of_points = anim.option("Number of points", 'The number of points around the circle.', 9, 2, 10000)
number_of_colors = anim.option('Number of colors', 'The number of colors used to draw the lines', 40, 1, 100)
point_multiplier = anim.option('Multiplier', 'The multiplication factor to go from one point to another.', 2, 2, 100)
line_width = anim.option('Line width', 'Width of the line between points.', 1., 0.1, 1000.)

#################################################################
#
# Points and geometries

radius = anim.outer_size / 2

def gen_points(count: int) -> List[anim.point]:
    points = []
    for i in range(count):
        theta = -math.pi / 2 + i * 2 * math.pi / count
        points.append(anim.point(math.cos(theta) * radius, math.sin(theta) * radius))
    return points

def gen_lines(multiplier: int, points: List[anim.point]) -> List[Tuple[anim.point]]:
    count = len(points)
    lines = [None] * count
    for p1 in range(0, count):
        p2 = (p1 * multiplier) % count
        lines[p1] = (points[p1], points[p2])
    return lines

def gen_lengths(lines: List[Tuple[anim.point]]) -> List[float]:
    dxs = [p1.x() - p2.x() for p1, p2 in lines]
    dys = [p1.y() - p2.y() for p1, p2 in lines]
    return [max(20., math.sqrt(dx * dx + dy * dy)) for dx, dy in zip(dxs, dys)]

def gen_colors(count: int) -> List[anim.color]:
    return [anim.color.fromHsvF(i * 1.0 / count, 1.0, 1.0, 0.5) for i in range(count)]

def get_color(length, min_length, max_length, colors):

    if min_length >= max_length:
        return colors[0]
    if length < min_length:
        return colors[0]
    if length > max_length:
        return colors[-1]
    length -= min_length
    length *= len(colors)
    length /= max_length - min_length
    return colors[math.floor(length) - 1]


#################################################################
#
# Actors

def generate_actors(animation: anim.animation, scene: anim.scene):
    point_count = number_of_points.value
    multiplier = point_multiplier.value
    color_count = number_of_colors.value
    width = line_width.value

    points = gen_points(point_count)
    lines = gen_lines(multiplier, points)
    lengths = gen_lengths(lines)
    colors = gen_colors(color_count)

    min_length = min(lengths)
    max_length = max(lengths)

    lengths_and_lines = [(length, line) for length, line in zip(lengths, lines)]
    lengths_and_lines.sort(key=lambda x: x[0])
    lengths_and_lines.reverse()

    circle = anim.actor('Circle', 'Circle on which the points lies', anim.create_circle(anim.point(0., 0.), radius, anim.pale_blue_color, 10.))
    point_actors = [anim.actor('Point', 'Points around the circle', anim.create_disk(pt, 10., anim.orange_color)) for pt in points]
    line_actors = [anim.actor('Line', 'Line linking two points that are ratio of the multipler', anim.create_line(*line, get_color(length, min_length, max_length, colors), width)) for length, line in lengths_and_lines]

    animation.add_actors([circle, point_actors, line_actors], scene)


#################################################################
#
# Shots

def generate_shots(animation: anim.animation):
    def prep_anim(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
        animator.animate_value(0., 1., 1)
    animation.add_shots(anim.shot('Vortex Maths', '', prep_anim))


#################################################################
#
# Animation

animation = anim.simple_animation.from_module(globals())
