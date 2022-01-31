import anim

from PySide6.QtCore import QPointF

from typing import List

#################################################################
#
# Description

name = "Quarter Geometric Sum"
description = "Mathologer."
loop = False
reset_on_change = False


#################################################################
#
# Actors

def create_square(base_point: anim.point, size: float, color) -> anim.polygon:
    return anim.create_filled_polygon([
        anim.relative_point(base_point,         0.,  0.),
        anim.relative_point(base_point, -size / 2., -size / 2.),
        anim.relative_point(base_point,         0., -size),
        anim.relative_point(base_point,  size / 2., -size / 2.),
    ], color)

def create_square_bases(base_point: anim.point, square_sizes: List[float]) -> List[anim.relative_point]:
    bases = []
    for size in square_sizes:
        base_point = anim.relative_point(base_point, 0., 0.)
        bases.append(base_point)
        base_point = anim.relative_point(base_point, 0., -size)
    return bases

def create_tower_squares(base_points: List[anim.point], square_sizes: List[float], color) -> List[anim.polygon]:
    squares = []
    for base, size in zip(base_points, square_sizes):
        squares.append(create_square(base, size, color))
    return squares

tower_count = 3
tower_height = 6
square_size = anim.outer_size / 4.
anim_duration = 3.

tower_colors = [ anim.orange_color, anim.blue_color, anim.red_color]

square_sizes = anim.geometric_serie(0., square_size, 1. / 2., tower_height)
tower_base_points = [anim.point(0., 0.) for _ in range(tower_count)]
tower_square_base_points = [create_square_bases(base, square_sizes) for base in tower_base_points]
tower_squares = [create_tower_squares(base, square_sizes, color) for base, color in zip(tower_square_base_points, tower_colors)]
tower_actors = [
    [anim.actor("Square", "Squares forming a geometric serie of sizes.", square) for square in tower]
    for tower in tower_squares
]

zero = QPointF(0., 0.)

central_tower_origin = zero
left_tower_origin  = QPointF(-square_size, 0.)
right_tower_origin = QPointF( square_size, 0.)

central_tower_base = tower_base_points[1]
central_tower_left_point = tower_squares[1][0].points[1]
central_tower_right_point = tower_squares[1][0].points[3]

left_tower_base = tower_base_points[0]
left_tower_base_points  = tower_square_base_points[0]

right_tower_base = tower_base_points[2]
right_tower_base_points = tower_square_base_points[2]

invisible_field = anim.actor("", "", anim.create_rect(-square_size * 1.7, -square_size * 2.5, square_size * 3.4, square_size * 2.5, anim.no_color, 0))
invisible_field.item.setPen(anim.no_pen)

def reset_relative_points():
    points = anim.find_all_of_type(globals(), anim.point)
    for pt in points:
        pt.reset()


#################################################################
#
# Shots

def prepare_place_towers_side_by_side(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    reset_relative_points()
    animator.animate_value(zero,  left_tower_origin, anim_duration, anim.anims.move_point( left_tower_base))
    animator.animate_value(zero, right_tower_origin, anim_duration, anim.anims.move_point(right_tower_base))
    scene.pointing_arrow.item.set_head(anim.relative_point(tower_squares[2][0].points[3]))
    animation.place_anim_pointing_arrow(zero, scene)

place_towers_side_by_side = anim.shot(
    "Side-by-side Towers",
    "Place the three square towers\n"
    "side-by-side.",
    prepare_place_towers_side_by_side)

def prepare_combine_towers(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    animator.animate_value( left_tower_origin, QPointF(central_tower_left_point ), anim_duration, anim.anims.move_point( left_tower_base))
    animator.animate_value(right_tower_origin, QPointF(central_tower_right_point), anim_duration, anim.anims.move_point(right_tower_base))

combine_towers = anim.shot(
    "Combine Towers",
    "Slide the side-towers up the sides\n"
    "of the central tower.",
    prepare_combine_towers)

def prepare_form_square(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    scene.pointing_arrow.item.set_head(anim.relative_point(tower_squares[2][1].points[3]))
    for size, left, right in zip(square_sizes[1:], left_tower_base_points[1:], right_tower_base_points[1:]):
        half_size = size / 2.
        animator.animate_value(zero, QPointF( half_size, half_size), anim_duration, anim.anims.move_point(left ))
        animator.animate_value(zero, QPointF(-half_size, half_size), anim_duration, anim.anims.move_point(right))

form_square = anim.shot(
    "Form a Square",
    "Slide all sub-squares of the\n"
    "side-towers to form a square.",
    prepare_form_square)

def prepare_break_up_square(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    for size, left, right in zip(square_sizes[1:], left_tower_base_points[1:], right_tower_base_points[1:]):
        half_size = size / 2.
        animator.animate_value(QPointF( half_size, half_size), zero, anim_duration, anim.anims.move_point(left ))
        animator.animate_value(QPointF(-half_size, half_size), zero, anim_duration, anim.anims.move_point(right))

break_up_square = anim.shot(
    "Deconstruct the Square",
    "Slide all sub-squares of the\n"
    "side-towers out of the square.",
    prepare_break_up_square)

def prepare_separate_towers(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    scene.pointing_arrow.item.set_head(anim.relative_point(tower_squares[2][0].points[3]))
    animator.animate_value(QPointF(central_tower_left_point ),  left_tower_origin, anim_duration, anim.anims.move_point( left_tower_base))
    animator.animate_value(QPointF(central_tower_right_point), right_tower_origin, anim_duration, anim.anims.move_point(right_tower_base))

separate_towers = anim.shot(
    "Separate Towers",
    "Slide the side-towers down the sides\n"
    "of the central tower.",
    prepare_separate_towers)


#################################################################
#
# Animation

animation = anim.simple_animation.from_module(globals())
