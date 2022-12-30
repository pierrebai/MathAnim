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

class points(anim.points):
    def __init__(self):
        super().__init__()
        self.text_height = 60.
        self.rows = 4

        self.rows_of_numbers = anim.deep_map(lambda i: str(i*2 + 1), anim.create_triangle_rows_of_numbers(self.rows))
        numbers_rect = [anim.scaling_text(number, anim.point(0., 0.), self.text_height).scene_rect() for number in anim.flatten(self.rows_of_numbers)]
        self.element_size = anim.static_point(
            max([number.width()  for number in numbers_rect]),
            max([number.height() for number in numbers_rect]))
        self.element_offset = anim.static_point(-self.element_size.x(), self.element_size.y() * 1.5)

        self.top = anim.point(0., 0.)

        self.rows_of_points = anim.create_rows_of_points(anim.create_triangle_rows_of_count(self.rows), self.top, self.element_size, self.element_offset)

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
            return anim.create_scaling_sans_text(number, pt, pts.text_height)

        self.rows_of_numbers = anim.deep_map(_create_label, pts.rows_of_numbers, pts.rows_of_points)

        self.number_highlight = anim.center_rectangle(pts.highlight_corner, pts.element_size * 1.2).fill(anim.no_color).outline(anim.pale_red).thickness(15.)

        self.background_rect = self.create_background_rect(pts)

geo: geometries = geometries(pts)


#################################################################
#
# Actors

actors = [
    [anim.actor('Number', '', number) for number in anim.flatten(geo.rows_of_numbers)],
    anim.actor('Highlight', '', geo.number_highlight),
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
    def reveal(item):
        anim.anim_reveal_item(animator, duration, item)
    anim.deep_map(reveal, geo.rows_of_numbers)

def highlight_numbers_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Odd numbers
    '''
    anim.anim_reveal_item(animator, quick_reveal_duration, geo.number_highlight)
    targets = [anim.static_point(pts.highlight_corner)] * 4
    for points, numbers in zip(pts.rows_of_points, geo.rows_of_numbers):
        count = 12 // len(points)
        for pt, number in zip(points, numbers):
            geo.number_highlight.center_on(number)
            targets.extend([anim.static_point(geo.number_highlight.center)] * count)
    pts.highlight_corner.set_absolute_point(targets[0])
    animator.animate_value(targets, duration * pts.rows / 2., anim.move_point(pts.highlight_corner))


#################################################################
#
# Animation

nicomachu_sums = anim.simple_animation.from_module(globals())
