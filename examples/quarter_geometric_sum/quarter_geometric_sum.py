import anim

from typing import List

#################################################################
#
# Description

name = "Quarter Geometric Sum"
description = "Mathologer video: https://www.youtube.com/watch?v=SOBz-aFOH2I"
loop = False
reset_on_change = False


#################################################################
#
# Points and geometries

def _create_square_bases(base_point: anim.point, square_sizes: List[float]) -> List[anim.relative_point]:
    bases = []
    for size in square_sizes:
        base_point = anim.relative_point(base_point, 0., 0.)
        bases.append(base_point)
        base_point = anim.relative_point(base_point, 0., -size)
    return bases

def _create_tower_squares(base_points: List[anim.point], square_sizes: List[float], color) -> List[anim.polygon]:
    squares = []
    for base, size in zip(base_points, square_sizes):
        squares.append(anim.create_losange(base, size).fill(color).outline(anim.black).thickness(0.).set_opacity(0.))
    return squares

tower_count = 3
tower_height = 8
losange_height = anim.outer_size / 4.
anim_duration = 1.

tower_colors = [ anim.red, anim.green, anim.blue ]
square_sizes = anim.geometric_serie(0., losange_height, 1. / 2., tower_height)
zero = anim.static_point(0., 0.)

tower_base_points = [anim.point(0., 0.) for _ in range(tower_count)]
tower_square_base_points = [_create_square_bases(base, square_sizes) for base in tower_base_points]
tower_squares = [_create_tower_squares(base, square_sizes, color) for base, color in zip(tower_square_base_points, tower_colors)]
tower_tip_points = [squares[-1].points[2] for squares in tower_squares]

central_tower_origin = zero
left_tower_origin  = anim.static_point(-losange_height, 0.)
right_tower_origin = anim.static_point( losange_height, 0.)

central_tower_base = tower_base_points[1]
central_tower_squares = tower_squares[1]
central_tower_left_point = central_tower_squares[0].points[1]
central_tower_right_point = central_tower_squares[0].points[3]

left_tower_base = tower_base_points[0]
left_tower_base_points  = tower_square_base_points[0]

right_tower_base = tower_base_points[2]
right_tower_base_points = tower_square_base_points[2]

quarter_texts = [
    anim.create_scaling_sans_text("1/4", square.points[0], size / 4, True).set_opacity(0.).center_on(square)
    for square, size in zip(central_tower_squares, square_sizes)
]

exponent_texts = [
    anim.create_scaling_sans_text(str(exponent+1), quarter.exponent_pos(), quarter.get_font_size() / 2, True).set_opacity(0.)
    for exponent, quarter in zip(range(1, tower_height), quarter_texts[1:])
]

base_squares = [squares[0] for squares in tower_squares]
base_square_texts = quarter_texts[0:1]

tower_texts = anim.flatten([quarter_texts, exponent_texts])
quarter_with_power_texts = anim.flatten([quarter_texts[1:], exponent_texts])

unit_square_base = anim.point(0., 0.)
unit_square = anim.create_losange(unit_square_base, losange_height * 2).set_opacity(0.).fill(anim.orange).outline(anim.black).thickness(0.)
unit_square.setZValue(-2.)
unit_text = anim.create_scaling_sans_text("1", unit_square.points[0], losange_height / 2, True).set_opacity(0.).center_on(unit_square)
unit_text.setZValue(-1.)
unit_square_and_text = [unit_square, unit_text]

third_texts = [anim.create_scaling_sans_text("1/3", anim.relative_point(tip), losange_height / 4, True).set_opacity(0.).place_above(tip) for tip in tower_tip_points]

equation_texts = anim.create_equation("1/3 = 1/4 + 1/4 ^ 2 + 1/4 ^ 3 + 1/4 ^ 4 + ...", anim.point(third_texts[1].top_left() + anim.static_point(-losange_height, -losange_height / 4)), losange_height / 6, True)


#################################################################
#
# Animation preparation

def _reset_relative_points():
    points = anim.find_all_of_type(globals(), anim.point)
    for pt in points:
        pt.reset()
    unit_text.set_sans_font(losange_height / 2, True)
    unit_text.center_on(unit_square)
    for text, tip in zip(third_texts, tower_tip_points):
        text.place_above(tip)

def _reset_opacities():
    for item in unit_square_and_text:
        item.set_opacity(0.)
    for item in third_texts:
        item.set_opacity(0.)
    for item in anim.flatten(tower_squares):
        item.set_opacity(1.)
    for item in tower_texts:
        item.set_opacity(0.)
    for item in equation_texts:
        item.set_opacity(0.)
    for item in anim.flatten(central_tower_squares):
        item.fill(anim.green)

def prepare_playing(animation: anim.animation, scene: anim.scene, animator: anim.animator):
    _reset_relative_points()
    _reset_opacities()
    # Note must reset the pointing arrow head to zero so it gets placed initially.
    animation.place_anim_pointing_arrow(zero, scene)


#################################################################
#
# Actors

tower_actors = [ anim.actor("Square", "", square) for square in anim.flatten(tower_squares) ]
unit_square_actor = anim.actor("Square", "Full square showing the total area.", unit_square)
quarter_actors = [ anim.actor("Fraction", "", text) for text in anim.flatten(quarter_texts) ]
exponent_actors = [ anim.actor("Fraction", "", text) for text in anim.flatten(exponent_texts) ]
unit_actor = anim.actor("Fraction", "", unit_text)
third_actors = [anim.actor("Fraction", "", text) for text in third_texts]
equation_actors = [anim.actor("Equation", "", eq) for eq in equation_texts]
invisible_field = anim.actor("", "", anim.create_invisible_rect(-losange_height * 1.7, -losange_height * 3, losange_height * 3.4, losange_height * 3))


#################################################################
#
# Shots

def place_towers_side_by_side_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Side-by-side Towers

    Consider these three square
    towers, placed side-by-side.
    """
    animator.animate_value([zero,  left_tower_origin,  left_tower_origin], anim_duration, anim.anims.move_point( left_tower_base))
    animator.animate_value([zero, right_tower_origin, right_tower_origin], anim_duration, anim.anims.move_point(right_tower_base))
    scene.pointing_arrow.item.set_head(anim.relative_point(tower_squares[2][0].points[3]))


def show_quarter_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Quarter Square

    Let's say the base of each
    tower has an area equal to
    a quarter.
    """
    scene.pointing_arrow.item.set_head(anim.relative_point(central_tower_squares[0].points[3]))
    animator.animate_value([0., 1.], anim_duration, anim.reveal_item(quarter_texts[0]))


def show_quarter_powers_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Powers of 1/4

    Each successive smaller
    square in the tower has
    an area that is a quarter
    of the previous square.
    """
    # Note: must set the head to a non-relative point before animating it.
    scene.pointing_arrow.item.set_head(anim.point(scene.pointing_arrow.item.head))
    animation.anim_pointing_arrow([anim.static_point(square.points[3]) for square in central_tower_squares], anim_duration, scene, animator)
    for item in quarter_with_power_texts:
        animator.animate_value([0., 1.], anim_duration, anim.reveal_item(item))


def form_square_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Form a Square

    When we combine all three
    towers, we form a square.
    """
    animator.animate_value([ left_tower_origin, anim.static_point(central_tower_left_point )], anim_duration, anim.anims.move_point( left_tower_base))
    animator.animate_value([right_tower_origin, anim.static_point(central_tower_right_point)], anim_duration, anim.anims.move_point(right_tower_base))
    scene.pointing_arrow.item.set_head(anim.relative_point(tower_squares[2][1].points[3]))
    for size, left, right in zip(square_sizes[1:], left_tower_base_points[1:], right_tower_base_points[1:]):
        half_size = size / 2.
        animator.animate_value([zero, anim.static_point( half_size, half_size)], anim_duration, anim.anims.move_point(left ))
        animator.animate_value([zero, anim.static_point(-half_size, half_size)], anim_duration, anim.anims.move_point(right))


def show_unit_square_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Unit Square

    It has the same area as the
    three towers.
    """
    scene.pointing_arrow.item.set_head(anim.relative_point(unit_text.exponent_pos()))
    for item in unit_square_and_text:
        animator.animate_value([0., 1., 1., 1.], anim_duration, anim.reveal_item(item))
    for item in anim.flatten(tower_squares):
        animator.animate_value([1., 0.], anim_duration / 4, anim.reveal_item(item))
    for item in tower_texts:
        animator.animate_value([1., 0.], anim_duration / 4., anim.reveal_item(item))

def show_quarters_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Unit Square

    Each base square had an
    area of a quarter...
    """
    scene.pointing_arrow.item.set_head(anim.relative_point(unit_text.exponent_pos()))
    animator.animate_value([1., 0.], anim_duration / 4, anim.reveal_item(unit_text))
    for item in anim.flatten(base_squares):
        animator.animate_value([0., 1.], anim_duration / 4, anim.reveal_item(item))
    for item in base_square_texts:
        animator.animate_value([0., 1.], anim_duration, anim.reveal_item(item))
    for item, color in zip(anim.flatten(base_squares), tower_colors):
        animator.animate_value([color, anim.orange], anim_duration / 4., anim.change_fill_color(item))


def show_unit_square_again_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Unit Square

    ... when we combine them,
    the big square has an area
    equal to one.
    """
    scene.pointing_arrow.item.set_head(anim.relative_point(unit_text.exponent_pos()))

    for item, color in zip(anim.flatten(base_squares), tower_colors):
        animator.animate_value([anim.orange, color], anim_duration, anim.change_fill_color(item))
    for item in anim.flatten(base_squares):
        animator.animate_value([1., 0.], anim_duration / 4, anim.reveal_item(item))
    for item in base_square_texts:
        animator.animate_value([1., 0.], anim_duration, anim.reveal_item(item))
    animator.animate_value([0., 1.], anim_duration / 4, anim.reveal_item(unit_text))
    animator.animate_value([losange_height / 2, losange_height / 4, losange_height / 4, losange_height / 4], anim_duration, anim.scale_text_item(unit_text))
    animator.animate_value([0., 1.], anim_duration, anim.center_text_item_on(unit_text, unit_square))


def hide_unit_square_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Unit Square

    ... when we combine them,
    the big square has an area
    equal to one.
    """
    scene.pointing_arrow.item.set_head(anim.relative_point(unit_text.exponent_pos()))

    text_pos = anim.static_point(unit_text.position)
    target_pos = anim.static_point(unit_text.place_above_pos(tower_tip_points[1]))
    animator.animate_value([text_pos, target_pos], anim_duration, anim.move_point(unit_text.position))

    animator.animate_value([1., 0.], anim_duration, anim.reveal_item(unit_square))

    for item in anim.flatten(tower_texts):
        animator.animate_value([0., 1.], anim_duration, anim.reveal_item(item))
    for item in anim.flatten(tower_squares):
        animator.animate_value([0., 1.], anim_duration, anim.reveal_item(item))
    

def break_up_square_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Break-up the Square

    When we separate the three
    towers, we see that each
    tower provided 1/3 of the
    total area.
    """
    scene.pointing_arrow.item.set_head(anim.relative_point(tower_squares[2][1].points[3]))
    for size, left, right in zip(square_sizes[1:], left_tower_base_points[1:], right_tower_base_points[1:]):
        half_size = size / 2.
        animator.animate_value([anim.static_point( half_size, half_size), zero], anim_duration, anim.anims.move_point(left ))
        animator.animate_value([anim.static_point(-half_size, half_size), zero], anim_duration, anim.anims.move_point(right))
    animator.animate_value([anim.static_point(central_tower_left_point ),  left_tower_origin], anim_duration, anim.anims.move_point( left_tower_base))
    animator.animate_value([anim.static_point(central_tower_right_point), right_tower_origin], anim_duration, anim.anims.move_point(right_tower_base))

    animator.animate_value([1., 0.], anim_duration, anim.reveal_item(unit_text))
    for item in third_texts:
        animator.animate_value([0., 1.], anim_duration, anim.reveal_item(item))


def isolate_central_tower_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Single Tower Area

    So, the central tower has
    a total area of 1/3.
    """
    scene.pointing_arrow.item.set_head(anim.relative_point(third_texts[1].exponent_pos()))
    animator.animate_value([left_tower_origin, zero], anim_duration, anim.anims.move_point( left_tower_base))
    animator.animate_value([right_tower_origin, zero], anim_duration, anim.anims.move_point(right_tower_base))
    animator.animate_value([1., 0.], anim_duration, anim.reveal_item(third_texts[0]))
    animator.animate_value([1., 0.], anim_duration, anim.reveal_item(third_texts[2]))
    for item in anim.flatten(tower_squares[0]):
        animator.animate_value([1., 0.], anim_duration, anim.reveal_item(item))
    for item in anim.flatten(tower_squares[2]):
        animator.animate_value([1., 0.], anim_duration, anim.reveal_item(item))


def final_equation_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Final Equation

    The sum of the areas of
    the squares is the sum
    of powers of 1/4, which
    means it is equal to 1/3.
    """
    scene.pointing_arrow.item.set_head(anim.relative_point(equation_texts[len(equation_texts) // 2].exponent_pos()))
    animator.animate_value([1., 0.], anim_duration, anim.reveal_item(third_texts[1]))
    for item in equation_texts:
        animator.animate_value([0., 1.], anim_duration, anim.reveal_item(item))


#################################################################
#
# Animation

quarter_geometric_sum = anim.simple_animation.from_module(globals())
