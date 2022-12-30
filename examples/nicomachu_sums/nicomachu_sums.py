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
            return anim.create_scaling_sans_text(number, anim.point(0., 0.), self.text_height)

        self.element_size = anim.maximum_size(anim.deep_map(_create_label, self.texts_spread))

        row_offset = anim.static_point(-self.element_size.x(), self.element_size.y() * 1.5)
        col_offset = anim.static_point(self.element_size.x() * 1.1, 0.)
        self.points_spread = anim.create_spread_of_points(self.triangle_spread, self.top, row_offset, col_offset)

        self.numbers_spread = anim.deep_filter(number_filter, self.texts_spread, self.triangle_spread)
        self.plusses_spread = anim.deep_filter(not_number_filter, self.texts_spread, self.triangle_spread)

        self.numbers_point_spread = anim.deep_filter(number_filter, self.points_spread, self.triangle_spread)
        self.plusses_point_spread = anim.deep_filter(not_number_filter, self.points_spread, self.triangle_spread)
        
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
            return anim.create_scaling_sans_text(number, pt, pts.text_height).center_on(pt)

        self.numbers_spread = anim.deep_map(_create_label, pts.numbers_spread, pts.numbers_point_spread)
        self.plusses_spread = anim.deep_map(_create_label, pts.plusses_spread, pts.plusses_point_spread)
        self.highlight = anim.center_rectangle(pts.highlight_corner, pts.element_size * 1.2).fill(anim.no_color).outline(anim.red).thickness(15.)
        self.background_rect = self.create_background_rect(pts)

geo: geometries = geometries(pts)


#################################################################
#
# Actors

actors = [
    [anim.actor('Equation', '', text) for text in anim.flatten(geo.numbers_spread)],
    [anim.actor('Equation', '', text) for text in anim.flatten(geo.plusses_spread)],
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
    '''
    Odd numbers
    '''
    def reveal(item: anim.scaling_text):
        anim.anim_reveal_item(animator, duration, item)
    anim.deep_map(reveal, geo.numbers_spread)

def highlight_numbers_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Odd numbers
    '''
    anim.anim_reveal_item(animator, quick_reveal_duration, geo.highlight)
    targets = [anim.static_point(pts.highlight_corner)] * 4
    for points, numbers in zip(pts.numbers_point_spread, geo.numbers_spread):
        count = 12 // len(points)
        for pt, number in zip(points, numbers):
            geo.highlight.center_on(number)
            targets.extend([anim.static_point(geo.highlight.center)] * count)
    pts.highlight_corner.set_absolute_point(targets[0])
    animator.animate_value(targets, duration * pts.rows / 2., anim.move_point(pts.highlight_corner))


#################################################################
#
# Animation

nicomachu_sums = anim.simple_animation.from_module(globals())
