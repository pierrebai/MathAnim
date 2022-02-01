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
# Points and geometries

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
        squares.append(anim.create_filled_losange(base, size, color))
    return squares

tower_count = 3
tower_height = 8
square_size = anim.outer_size / 4.
anim_duration = 3.

tower_colors = [ anim.red_color, anim.green_color, anim.blue_color ]

square_sizes = anim.geometric_serie(0., square_size, 1. / 2., tower_height)
tower_base_points = [anim.point(0., 0.) for _ in range(tower_count)]
tower_square_base_points = [create_square_bases(base, square_sizes) for base in tower_base_points]
tower_squares = [create_tower_squares(base, square_sizes, color) for base, color in zip(tower_square_base_points, tower_colors)]
tower_tip_points = [squares[-1].points[2] for squares in tower_squares]
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

quarter_texts = [ [
        anim.create_scaling_sans_text("1/4", square.points[0], size / 4).center_on(square)
        for square, size in zip(tower, square_sizes)
    ]
    for tower in tower_squares
]

exponent_texts = [ [
        anim.create_scaling_sans_text(str(exponent+1), quarter.exponent_pos(), quarter.get_font_size() / 2)
        for exponent, quarter in zip(range(1, tower_height), tower[1:])
    ]
    for tower in quarter_texts
]

tower_texts = anim.flatten([quarter_texts, exponent_texts])
towers_and_texts = anim.flatten([tower_squares, quarter_texts, exponent_texts])

unit_square_base = anim.point(0., 0.)
unit_square = anim.create_filled_losange(unit_square_base, square_size * 2, anim.orange_color)
unit_text = anim.create_scaling_sans_text("1", unit_square.points[0], square_size / 2).center_on(unit_square)
unit_square_and_text = [unit_square, unit_text]

third_texts = [anim.create_scaling_sans_text("1/3", tip, square_size / 4).place_above(tip) for tip in tower_tip_points]

equation_texts = anim.create_equation("1/3 = 1/4 + 1/4 ^ 2 + 1/4 ^ 3 + 1/4 ^ 4 + ...", anim.point(third_texts[0]._pos + QPointF(-square_size, -square_size / 4)), square_size / 6)


def reset_relative_points():
    points = anim.find_all_of_type(globals(), anim.point)
    for pt in points:
        pt.reset()

def reset_opacities():
    for item in unit_square_and_text:
        item.setOpacity(0.)
    for item in third_texts:
        item.setOpacity(0.)
    for item in anim.flatten(tower_squares):
        item.setOpacity(1.)
    for item in tower_texts:
        item.setOpacity(0.)
    for item in equation_texts:
        item.setOpacity(0.)

reset_relative_points()
reset_opacities()


#################################################################
#
# Actors

tower_actors = [ anim.actor("Square", "", square) for square in anim.flatten(tower_squares) ]
unit_square_actor = anim.actor("Square", "Full square showing the total area.", unit_square)
quarter_actors = [ anim.actor("Fraction", "", text) for text in anim.flatten(quarter_texts) ]
exponent_actors = [ anim.actor("Fraction", "", text) for text in anim.flatten(exponent_texts) ]
unit_actor = anim.actor("Fraction", "", unit_text)
third_actors = [anim.actor("Fraction", "", third) for third in third_texts]
equation_actors = [anim.actor("Equation", "", eq) for eq in equation_texts]
invisible_field = anim.actor("", "", anim.create_invisible_rect(-square_size * 1.7, -square_size * 3, square_size * 3.4, square_size * 3))


#################################################################
#
# Shots

def place_towers_side_by_side_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Side-by-side Towers

    Place three square towers
    side-by-side.
    """
    reset_relative_points()
    reset_opacities()
    animator.animate_value(zero,  left_tower_origin, anim_duration, anim.anims.move_point( left_tower_base))
    animator.animate_value(zero, right_tower_origin, anim_duration, anim.anims.move_point(right_tower_base))
    scene.pointing_arrow.item.set_head(anim.relative_point(tower_squares[2][0].points[3]))
    animation.place_anim_pointing_arrow(zero, scene)

def combine_towers_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Combine Towers

    Slide the side-towers up the
    sides of the central tower
    to show they fit together.
    """
    animator.animate_value( left_tower_origin, QPointF(central_tower_left_point ), anim_duration, anim.anims.move_point( left_tower_base))
    animator.animate_value(right_tower_origin, QPointF(central_tower_right_point), anim_duration, anim.anims.move_point(right_tower_base))

def form_square_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Form a Square

    Slide all sub-squares of
    the side-towers to show
    they combine with the central
    tower to form a complete square.
    """
    scene.pointing_arrow.item.set_head(anim.relative_point(tower_squares[2][1].points[3]))
    for size, left, right in zip(square_sizes[1:], left_tower_base_points[1:], right_tower_base_points[1:]):
        half_size = size / 2.
        animator.animate_value(zero, QPointF( half_size, half_size), anim_duration, anim.anims.move_point(left ))
        animator.animate_value(zero, QPointF(-half_size, half_size), anim_duration, anim.anims.move_point(right))

def show_unit_square_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Show Equivalent Square

    Show the unit square that
    has an area equal to the
    combined tower.

    The base-square of each
    tower is a quarter of the
    full unit square.
    """
    scene.pointing_arrow.item.set_head(anim.relative_point(unit_square.points[3]))
    for item in unit_square_and_text:
        animator.animate_value(0., 1., anim_duration, anim.reveal_item(item))
    for item in quarter_texts:
        animator.animate_value(0., 1., anim_duration, anim.reveal_item(item[0]))
    for item in anim.flatten(tower_squares):
        animator.animate_value(1., 0., anim_duration, anim.reveal_item(item))

def hide_unit_square_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Hide Equivalent Square

    Show again the towers,
    underlining that each
    one represent a third
    of the total unit area.

    Show that as we go up
    in each tower, each
    smaller square is a
    quarter the size of
    the preceding square.
    """
    for item in unit_square_and_text:
        animator.animate_value(1., 0., anim_duration, anim.reveal_item(item))
    for item in towers_and_texts:
        animator.animate_value(0., 1., anim_duration, anim.reveal_item(item))
    for item in third_texts:
        animator.animate_value(0., 1., anim_duration, anim.reveal_item(item))

def break_up_square_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Deconstruct the Square

    Slide all sub-squares
    of the side-towers out
    of the unit square.
    """
    scene.pointing_arrow.item.set_head(anim.relative_point(tower_squares[2][1].points[3]))
    for size, left, right in zip(square_sizes[1:], left_tower_base_points[1:], right_tower_base_points[1:]):
        half_size = size / 2.
        animator.animate_value(QPointF( half_size, half_size), zero, anim_duration, anim.anims.move_point(left ))
        animator.animate_value(QPointF(-half_size, half_size), zero, anim_duration, anim.anims.move_point(right))

def separate_towers_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Separate Towers
    
    Slide the side-towers
    down the sides of the
    central tower.
    """
    scene.pointing_arrow.item.set_head(anim.relative_point(tower_squares[2][0].points[3]))
    animator.animate_value(QPointF(central_tower_left_point ),  left_tower_origin, anim_duration, anim.anims.move_point( left_tower_base))
    animator.animate_value(QPointF(central_tower_right_point), right_tower_origin, anim_duration, anim.anims.move_point(right_tower_base))

def final_equation_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Show the final equation

    The sum of the area of
    the squares of one tower
    is equal to one third of
    the unit area.

    But the sum of the area
    of the squares is also
    the sum of powers of 1/4.
    """
    scene.pointing_arrow.item.set_head(anim.relative_point(equation_texts[-1]._pos))
    for item in third_texts:
        animator.animate_value(1., 0., anim_duration, anim.reveal_item(item))
    for item in tower_texts:
        animator.animate_value(1., 0., anim_duration, anim.reveal_item(item))
    for item in equation_texts:
        animator.animate_value(0., 1., anim_duration, anim.reveal_item(item))


#################################################################
#
# Animation

animation = anim.simple_animation.from_module(globals())
