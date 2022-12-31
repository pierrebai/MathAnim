import anim

from typing import List as _List
from math import factorial

#################################################################
#
# Description

name = "Nicomachu's Gem"
description = 'Mathologer video: https://www.youtube.com/watch?v=WY5X_3q80WY'
loop = False
reset_on_change = False
has_pointing_arrow = False

duration = 2.
short_duration = duration / 2.
long_duration = duration * 2.
quick_reveal_duration = duration / 8.

#################################################################
#
# Points

def is_number(item: anim.spread_item) -> bool:
    return not item.column % 2

def number_filter(value, item: anim.spread_item):
    return value if is_number(item) else None

def not_number_filter(value, item: anim.spread_item):
    return None if is_number(item) else value

class points(anim.points):
    def __init__(self):
        super().__init__()
        self.text_height = 60.
        self.rows = 4

        self.triangle_spread = anim.create_triangle_odd_spread(self.rows)
        self.texts_spread = anim.deep_map(lambda item: str(item.index * 2 + 1) if is_number(item) else '+', self.triangle_spread)

        self.top = anim.point(0., 0.)

        def _create_label(number: str):
            return anim.create_scaling_sans_text(number, anim.point(0., 0.), self.text_height, True)

        self.element_size = anim.maximum_size(anim.deep_map(_create_label, self.texts_spread))

        self.row_offset = anim.static_point(-self.element_size.x(), self.element_size.y() * 1.5)
        self.col_offset = anim.static_point(self.element_size.x(), 0.)
        self.points_spread = anim.create_spread_of_points(self.triangle_spread, self.top, self.row_offset, self.col_offset)

        self.numbers_spread = anim.deep_filter(number_filter, self.texts_spread, self.triangle_spread)
        self.plusses_spread = anim.deep_filter(not_number_filter, self.texts_spread, self.triangle_spread)

        self.numbers_point_spread = anim.deep_filter(number_filter, self.points_spread, self.triangle_spread)
        self.plusses_point_spread = anim.deep_filter(not_number_filter, self.points_spread, self.triangle_spread)

        last_number_point = anim.last_of(self.numbers_point_spread) + self.col_offset * 2

        self.equals_point = [anim.point(last_number_point.x(), pts[-1].y()) for pts in self.numbers_point_spread]
        
        self.highlight_corner = anim.relative_point(self.top, anim.point(0., self.text_height * -3.))

pts: points = points()


#################################################################
#
# Geometries

class geometries(anim.geometries):
    label_size = 50.

    def __init__(self, pts: points):
        super().__init__()

        def _create_label(number: str, pt: anim.point):
            return anim.create_scaling_sans_text(number, pt, pts.text_height, True).center_on(pt).align_on_center()

        self.numbers_spread = anim.deep_map(_create_label, pts.numbers_spread, pts.numbers_point_spread)
        self.plusses_spread = anim.deep_map(_create_label, pts.plusses_spread, pts.plusses_point_spread)
        self.highlight = anim.center_rectangle(pts.highlight_corner, pts.element_size * 1.2).fill(anim.no_color).outline(anim.red).thickness(15.)
        self.etc = _create_label('etc.', anim.point(0., pts.row_offset.y() * pts.rows))

        self.equals_power = [_create_label(f'= {i ** 3}', pt).align_on_left() for i, pt in enumerate(pts.equals_point)]
        self.equals_cube  = [_create_label(f'= {i}³',     pt).align_on_left() for i, pt in enumerate(pts.equals_point)]

        self.background_rect = self.create_background_rect(pts)

    def reset(self):
        super().reset()
        for number in anim.flatten(self.numbers_spread):
            number.fill(anim.black)

geo: geometries = geometries(pts)

colors = [anim.dark_red, anim.dark_green, anim.dark_blue, anim.dark_sable]

#################################################################
#
# Actors

actors = [
    [anim.actor('Equation', '', text) for text in anim.flatten(geo.numbers_spread)],
    [anim.actor('Equation', '', text) for text in anim.flatten(geo.plusses_spread)],
    [anim.actor('Equation', '', text) for text in anim.flatten(geo.equals_cube)],
    [anim.actor('Equation', '', text) for text in anim.flatten(geo.equals_power)],
    anim.actor('Equation', '', geo.etc),
    anim.actor('Highlight', '', geo.highlight),
    anim.actor('Background', '', geo.background_rect),
]


#################################################################
#
# Prepare animation

def prepare_playing(animation: anim.animation, scene: anim.scene, animator: anim.animator):
    pts.reset()
    geo.reset()

def reset(animation: anim.animation, scene: anim.scene, animator: anim.animator):
    pts.reset()
    geo.reset()


#################################################################
#
# Shots

def show_triangle_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    def reveal(item: anim.scaling_text):
        anim.anim_reveal_item(animator, duration, item)
    anim.deep_map(reveal, geo.numbers_spread)

def highlight_numbers_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    anim.anim_reveal_item(animator, quick_reveal_duration, geo.highlight)
    targets = [anim.static_point(pts.highlight_corner)] * 4
    for points, numbers in zip(pts.numbers_point_spread, geo.numbers_spread):
        count = 12 // len(points)
        for pt, number in zip(points, numbers):
            geo.highlight.center_on(number)
            targets.extend([anim.static_point(geo.highlight.center)] * count)
    pts.highlight_corner.set_absolute_point(targets[0])
    animator.animate_value(targets, duration * pts.rows / 2., anim.move_point(pts.highlight_corner))

def etc_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    anim.anim_hide_item(animator, quick_reveal_duration, geo.highlight)
    anim.anim_reveal_item(animator, duration, geo.etc)

def _create_sub_number_shot(numbers, plusses, color):
    def _sub_number_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
        for plus in plusses:
            anim.anim_reveal_item(animator, quick_reveal_duration, plus)
        for number in numbers:
            animator.animate_value([anim.black, color], quick_reveal_duration, anim.change_fill_color(number))
    return anim.anim_description.create_shot(_sub_number_shot)

def add_numbers_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    shots = [_create_sub_number_shot(numbers, plusses, color)  for numbers, plusses, color in zip(geo.numbers_spread, geo.plusses_spread, colors)]
    animation.add_next_shots(shots)

def _create_cube_shot(cube, pt, color):
    def _cube_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
        anim.anim_reveal_item(animator, quick_reveal_duration, cube)
        cube.fill(color)
        animator.animate_value([anim.static_point(pt + anim.point(100., 0.)), anim.static_point(pt)], duration, anim.move_point(pt))
    return anim.anim_description.create_shot(_cube_shot)

def _create_power_shot(cube, power, color):
    def _power_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
        anim.anim_hide_item(animator, quick_reveal_duration, cube)
        power.fill(color)
        anim.anim_reveal_item(animator, quick_reveal_duration, power)
    return anim.anim_description.create_shot(_power_shot)

def show_cubes_and_powers_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    cubes_shot = [_create_cube_shot(cube, pt, color) for cube, pt, color in zip(geo.equals_cube, pts.equals_point, colors)]
    powers_shot = [_create_power_shot(cube, power, color) for cube, power, color in zip(geo.equals_cube, geo.equals_power, colors)]
    for cube, power in zip(reversed(cubes_shot), reversed(powers_shot)):
        animation.add_next_shots([cube, power])


#################################################################
#
# Animation

nicomachu_sums = anim.simple_animation.from_module(globals())
