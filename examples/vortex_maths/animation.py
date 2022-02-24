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
point_multiplier = anim.option('Multiplier', 'The multiplication factor to go from one point to another.', 2, 2, 100)
line_width = anim.option('Line width', 'Width of the line between points.', 10, 0, 200)

color_gradient = anim.option('Color gradient', 'Color swatches applied to lines according to their length', 'Rainbow', list(anim.gradients.keys()))
interpolate_colors = anim.option('Interpolate colors', 'Interpolate the colors to have a smoother gradient', True)
reverse_color_gradient = anim.option('Reverse colors', 'Reverse the order of colors in the gradient', False)
black_background = anim.option('Black background', 'Use a black background', False)


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

def gen_texts(points: List[anim.point]) -> List[anim.scaling_text]:
    texts = []
    count = len(points)
    zero = anim.point(0., 0.)
    for i in range(count):
        theta = -math.pi / 2 + i * 2 * math.pi / count
        text = anim.scaling_text(str(i), points[i], 20)
        text.place_around(points[i], theta, 40)
        texts.append(text)
    return texts

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
    return [max(10., math.sqrt(dx * dx + dy * dy)) for dx, dy in zip(dxs, dys)]


#################################################################
#
# Actors

def generate_actors(animation: anim.animation, scene: anim.scene):
    point_count = number_of_points.value
    multiplier = point_multiplier.value
    width = line_width.value / 10.

    points = gen_points(point_count)
    texts = gen_texts(points)
    lines = gen_lines(multiplier, points)
    lengths = gen_lengths(lines)

    colors = anim.gradients[color_gradient.value].interpolated(interpolate_colors.value)
    if reverse_color_gradient.value:
        colors = colors.reversed()

    min_length = min(lengths)
    max_length = max(lengths)

    lengths_and_lines = [(length, line) for length, line in zip(lengths, lines)]
    lengths_and_lines.sort(key=lambda x: x[0])
    lengths_and_lines.reverse()

    background_color = anim.black_color if black_background.value else anim.white_color
    background = anim.actor('Background', 'Background on which all the rest is drawn', anim.create_disk(anim.point(0., 0.), radius * 1.05, background_color))

    circle = anim.actor('Circle', 'Circle on which the points lies', anim.create_circle(anim.point(0., 0.), radius, anim.pale_blue_color, 10.))

    if len(points) <= 60:
        text_actors = [anim.actor('Number', 'The numbers corresponding to each point around teh circle', text) for text in texts]
    else:
        text_actors = []
        
    if len(points) <= 360:
        point_actors = [anim.actor('Point', 'Points around the circle', anim.create_disk(pt, 10., anim.orange_color)) for pt in points]
    else:
        point_actors = []

    line_actors = [anim.actor('Line', 'Line linking two points that are ratio of the multipler', anim.create_line(*line, colors.get_color(length, min_length, max_length), width)) for length, line in lengths_and_lines]

    animation.add_actors([background, circle, point_actors, text_actors, line_actors], scene)


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
