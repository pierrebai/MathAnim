import anim

from typing import List as _List
from math import factorial
from itertools import product

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
        self.cube_radius = 40.

        self.rows = 4

        self.triangle_spread = anim.create_triangle_odd_spread(self.rows)
        self.texts_spread = anim.deep_map(lambda item: str(item.row * 2 + item.column + 1) if is_number(item) else '+', self.triangle_spread)

        self.top = anim.point(0., 0.)

        def _create_label(number: str):
            return anim.create_sans_bold_text(number, anim.point(0., 0.), self.text_height)

        self.element_size = anim.maximum_size(anim.deep_map(_create_label, self.texts_spread))

        self.row_offset = anim.static_point(-self.element_size.x(), self.element_size.y() * 1.5)
        self.col_offset = anim.static_point(self.element_size.x(), 0.)
        self.points_spread = anim.create_spread_of_points(self.triangle_spread, self.top, self.row_offset, self.col_offset)

        self.numbers_spread = anim.deep_filter(number_filter, self.texts_spread, self.triangle_spread)
        self.plusses_spread = anim.deep_filter(not_number_filter, self.texts_spread, self.triangle_spread)

        self.numbers_point_spread = anim.deep_filter(number_filter, self.points_spread, self.triangle_spread)
        self.plusses_point_spread = anim.deep_filter(not_number_filter, self.points_spread, self.triangle_spread)

        last_number_point = anim.last_of(self.numbers_point_spread) + self.col_offset * 2

        self.cube_eqs_point  = [anim.point(last_number_point.x(), pts[-1].y()) for pts in self.numbers_point_spread]
        self.power_eqs_point = [anim.point(last_number_point.x(), pts[-1].y()) for pts in self.numbers_point_spread]
        
        self.highlight_corner = anim.relative_point(self.top, anim.point(0., self.text_height * -3.))

        self.square_deltas = anim.static_point(50., 50.), anim.static_point(-50., 50.)
        self.square_tip_point = anim.static_point(500., -300.)

pts: points = points()


#################################################################
#
# Geometries

colors = [anim.dark_red, anim.dark_green, anim.dark_blue, anim.dark_sable]

class geometries(anim.geometries):
    def __init__(self, pts: points):
        super().__init__()

        def _create_label(label: str, pt: anim.point):
            return anim.create_sans_bold_text(label, pt, pts.text_height).center_on(pt).align_on_center()

        self.numbers_spread = anim.deep_map(_create_label, pts.numbers_spread, pts.numbers_point_spread)
        self.plusses_spread = anim.deep_map(_create_label, pts.plusses_spread, pts.plusses_point_spread)
        self.highlight = anim.center_rectangle(pts.highlight_corner, pts.element_size * 1.2).fill(anim.no_color).outline(anim.red).thickness(15.)
        self.etc = _create_label('etc.', anim.point(0., pts.row_offset.y() * pts.rows))

        self.cube_eqs  = [self._create_colored_eq(f' = {i ** 3}', pt, pts.text_height, i-1) for i, pt in enumerate(pts.cube_eqs_point,  1)]
        self.power_eqs = [self._create_colored_eq(f' = {i}³',     pt, pts.text_height, i-1) for i, pt in enumerate(pts.power_eqs_point, 1)]

        why_point = anim.relative_point(self.power_eqs[0][-1].middle_right(), anim.point(80., 0.))
        self.here_is_why = anim.create_sans_bold_text('Here\nis\nwhy', why_point, pts.text_height * 1.5)

        proof_point = anim.relative_point(self.power_eqs[0][-1].middle_right(), anim.point(80., 0.))
        self.proof = anim.create_sans_bold_text('The\ncubes\nsquare\ntriangle\nproof', proof_point, pts.text_height)

        cubes_points = [anim.point(x, 100.) for x in [-400., -250., -50., 200.]]
        self.cubes = [anim.cube_of_cubes(size, pt, pts.cube_radius, 0.6).fill(color) for size, pt, color in zip(range(1, 5), cubes_points, colors)]

        self.top_sides   = [anim.deep_map(lambda cube: cube.sub_items[0],  cube_of_cubes.cubes) for cube_of_cubes in self.cubes]
        self.other_sides = [anim.deep_map(lambda cube: cube.sub_items[1:], cube_of_cubes.cubes) for cube_of_cubes in self.cubes]

        self.right_rects = [anim.rectangle(anim.point(0., 0.), anim.point(1., 1)).fill(color).outline(anim.no_color) for color in colors]

        self.right_limit = anim.rectangle(anim.point(0., 0.), anim.point(1400, 10.))

        self.background_rect = self.create_background_rect(pts, anim.static_point(0.1, 0.1), anim.static_point(0.1, 0.1))

    @staticmethod
    def _create_colored_eq(label: str, pt: anim.point, font_size: float, which_color: int):
        def _sub_text_creator(label: str, pt: anim.point, font_size: float):
            return anim.create_sans_bold_text(label, pt, font_size).align_on_left()
        text_creator = anim.create_colored_numbers_creator(colors[which_color], _sub_text_creator)
        return anim.create_equation(label, pt, font_size, text_creator)

    def reset(self):
        super().reset()
        for number in anim.flatten(self.numbers_spread):
            number.fill(anim.black)

geo: geometries = geometries(pts)


#################################################################
#
# Actors

actors = [
    [anim.actor('Equation', '', text) for text in anim.flatten(geo.numbers_spread)],
    [anim.actor('Equation', '', text) for text in anim.flatten(geo.plusses_spread)],
    [anim.actor('Equation', '', text) for text in anim.flatten(geo.cube_eqs)],
    [anim.actor('Equation', '', text) for text in anim.flatten(geo.power_eqs)],
    [anim.actor('Equation', '', rect) for rect in geo.right_rects],
    anim.actor('Explanation', '', geo.etc),
    anim.actor('Explanation', '', geo.here_is_why),
    anim.actor('Explanation', '', geo.proof),
    [[anim.actor('Cube', '', cube) for cube in cube_of_cubes.sub_items] for cube_of_cubes in geo.cubes],
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
    #geo.background_rect.set_opacity(1.)
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

def _create_add_number_shot(numbers, plusses, color):
    def _sub_number_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
        for plus in plusses:
            anim.anim_reveal_item(animator, quick_reveal_duration, plus)
        for number in numbers:
            animator.animate_value([anim.black] + [color] * 3, short_duration, anim.change_fill_color(number))
    return anim.anim_description.create_shot(_sub_number_shot)

def add_numbers_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    shots = [_create_add_number_shot(numbers, plusses, color)  for numbers, plusses, color in zip(geo.numbers_spread, geo.plusses_spread, colors)]
    animation.add_next_shots(shots)

def _create_cube_shot(cube_eq: _List[anim.scaling_text], pt: anim.point):
    def _cube_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
        for item in cube_eq:
            anim.anim_reveal_item(animator, quick_reveal_duration, item)
        from_pt = anim.static_point(pt + anim.point(300., 0.))
        dest_pt = anim.static_point(pt)
        animator.animate_value([from_pt, dest_pt, dest_pt], short_duration, anim.move_point(pt))
    return anim.anim_description.create_shot(_cube_shot)

def _create_power_shot(cube_eq: _List[anim.scaling_text], power_eq: _List[anim.scaling_text], pt: anim.point):
    def _power_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
        for item in power_eq:
            anim.anim_reveal_item(animator, quick_reveal_duration, item)
        from_pt = anim.static_point(pt + anim.point(300., 0.))
        dest_x  = cube_eq[-1].scene_rect().topRight().x()
        dest_pt = anim.static_point(dest_x, pt.original_point.y())
        animator.animate_value([from_pt, dest_pt, dest_pt], short_duration, anim.move_point(pt))
    return anim.anim_description.create_shot(_power_shot)

def _create_replace_power_shot(cube_eq: _List[anim.scaling_text], pt: anim.point):
    def _power_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
        for item in cube_eq:
            anim.anim_hide_item(animator, quick_reveal_duration, item)
        from_pt = anim.static_point(pt)
        dest_pt = anim.static_point(pt.original_point)
        animator.animate_value([from_pt, dest_pt, dest_pt], short_duration, anim.move_point(pt))
    return anim.anim_description.create_shot(_power_shot)

def show_cubes_and_powers_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    cubes_shot = [_create_cube_shot(cube, pt) for cube, pt in zip(geo.cube_eqs, pts.cube_eqs_point)]
    powers_shot = [_create_power_shot(cube, power, pt) for cube, power, pt in zip(geo.cube_eqs, geo.power_eqs, pts.power_eqs_point)]
    replaces_shot = [_create_replace_power_shot(cube, pt) for cube, pt in zip(geo.cube_eqs, pts.power_eqs_point)]
    animation.add_next_shots(anim.interleave_lists([cubes_shot, powers_shot, replaces_shot]))

def etc_power_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    anim.anim_ondulate_text_size(animator, duration, geo.etc)

def here_is_why_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    anim.anim_reveal_item(animator, duration, geo.here_is_why)
    anim.anim_ondulate_text_size(animator, short_duration, geo.here_is_why, 1.3)

def proof_name_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    anim.anim_hide_item(animator, short_duration, geo.here_is_why)
    anim.anim_reveal_item(animator, duration, geo.proof)
    anim.anim_ondulate_text_size(animator, short_duration, geo.proof, 1.3)

def show_cubes_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    anim.anim_hide_item(animator, quick_reveal_duration, geo.proof)
    anim.anim_hide_item(animator, quick_reveal_duration, geo.etc)
    for label in anim.flatten(geo.numbers_spread):
        anim.anim_hide_item(animator, quick_reveal_duration, label)
    for label in anim.flatten(geo.plusses_spread):
        anim.anim_hide_item(animator, quick_reveal_duration, label)

    _, dy, dz = anim.last_of(geo.cubes).get_deltas()
    which_cubes = [0, 1, 1, 1]
    for which_cube, power_eq, cube in zip(which_cubes, geo.power_eqs, geo.cubes):
        anim.anim_hide_item(animator, quick_reveal_duration, power_eq[0])
        from_pt = anim.static_point(power_eq[1].position)
        dest_pt = anim.static_point(cube.cubes[which_cube][-1][0].sub_items[0].points[-1] + dy * 2. - dz * 2.)
        animator.animate_value([from_pt, dest_pt, dest_pt], duration, anim.move_absolute_point(power_eq[1].position))
    for cube in anim.flatten(geo.cubes):
        anim.anim_reveal_item(animator, duration, cube)

def first_split_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    _, _, dz = anim.last_of(geo.cubes).get_deltas()
    for which, power_eq in enumerate(geo.power_eqs):
        from_pt = anim.static_point(power_eq[1].position)
        dest_pt = anim.static_point(from_pt - which * dz)
        animator.animate_value([from_pt, dest_pt, dest_pt], duration, anim.move_absolute_point(power_eq[1].position))
    for cube in geo.cubes:
        z_slices = cube.get_z_slices()
        z_count = len(z_slices)
        for z, slice in enumerate(z_slices):
            for cube in anim.flatten(slice):
                pt = cube.position
                from_pt = anim.static_point(pt)
                dest_pt = anim.static_point(from_pt - (z_count - z - 1) * dz)
                animator.animate_value([from_pt, dest_pt, dest_pt], duration, anim.move_absolute_point(pt))

def second_split_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    dx, dy, _ = anim.last_of(geo.cubes).get_deltas()
    for cube in geo.cubes:
        count = len(cube.cubes)
        if count % 2:
            continue
        z_slice = cube.get_z_slices()[0]
        for x, x_cubes in enumerate(z_slice):
            for y, y_cube in enumerate(x_cubes):
                delta = anim.static_point(0., 0.)
                delta += dx / 3. * (-1. if x < count // 2 else 1.)
                delta += dy / 3. * (-1. if y < count // 2 else 1.)
                pt = y_cube.position
                from_pt = anim.static_point(pt)
                dest_pt = anim.static_point(from_pt + delta)
                animator.animate_value([from_pt, dest_pt, dest_pt], duration, anim.move_absolute_point(pt))

def _get_square_destinations():
    """
    Destination to deconstruct the cube of cubes into a square.

    Format: (from cube #, from 3D coordinates, 2D slice, destination coordinates)
            3D coordinates are in cube coordinates, but destinations coordinates
            are with the origin at the small 1x1x1 red cube.
    """
    return [
        (0, (0, 0, 0), (1, 1), (0, 0)),
        (1, (0, 0, 0), (1, 1), (0, 2)),
        (1, (0, 1, 0), (1, 1), (0, 1)),
        (1, (1, 0, 0), (1, 1), (2, 0)),
        (1, (1, 1, 0), (1, 1), (1, 0)),
        (1, (0, 0, 1), (2, 2), (1, 2)),
        (2, (0, 0, 0), (3, 3), (0, 5)),
        (2, (0, 0, 1), (3, 3), (3, 5)),
        (2, (0, 0, 2), (3, 3), (3, 2)),
        (3, (0, 0, 0), (2, 2), (0, 9)),
        (3, (0, 2, 0), (2, 2), (0, 7)),
        (3, (2, 0, 0), (2, 2), (6, 1)),
        (3, (2, 2, 0), (2, 2), (8, 1)),
        (3, (0, 0, 1), (4, 4), (2, 9)),
        (3, (0, 0, 2), (4, 4), (6, 9)),
        (3, (0, 0, 3), (4, 4), (6, 5)),
    ]

def lay_down_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    destinations = _get_square_destinations()
    dx, dy, dz = geo.cubes[0].get_deltas()
    base_dest = anim.static_point(anim.first_of(geo.cubes[0].cubes).position)
    for cube, cube_coord, slice, dest_coord in destinations:
        cube_of_cubes = geo.cubes[cube]
        cube_z = cube_coord[2]
        for cube_x, cube_y in product(range(slice[0]), range(slice[1])):
            dest_x = dest_coord[0] + cube_x
            dest_y = dest_coord[1] - cube_y

            cube = cube_of_cubes.cubes[cube_coord[0] + cube_x][cube_coord[1] + cube_y][cube_z]

            move_pt = cube.position
            from_pt = anim.static_point(move_pt)
            dest_pt = base_dest + dx * dest_x - dy * dest_y

            animator.animate_value([from_pt, dest_pt, dest_pt], duration, anim.move_absolute_point(move_pt))
            cube.set_z_order(dest_y + 10. * (10 - dest_x))

    for which, power_eq in enumerate(geo.power_eqs):
        from_pt = anim.static_point(power_eq[1].position)
        dest_pt = anim.static_point(base_dest - dz * 4 + (which -1) * 3 * dx)
        power_eq[1].set_opacity(1.) # TODO remove when in full demonstration mode.
        animator.animate_value([from_pt, dest_pt, dest_pt], duration, anim.move_absolute_point(power_eq[1].position))


def make_square_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    destinations = _get_square_destinations()
    dx, dy = pts.square_deltas
    for which_cube, cube_coord, slice, dest_coord in destinations:
        top_sides   = geo.top_sides[which_cube]
        other_sides = geo.other_sides[which_cube]

        cube_z = cube_coord[2]
        for cube_x, cube_y in product(range(slice[0]), range(slice[1])):
            dest_x = dest_coord[0] + cube_x
            dest_y = dest_coord[1] - cube_y

            top_side = top_sides[cube_coord[0] + cube_x][cube_coord[1] + cube_y][cube_z]

            tip_position = anim.static_point(pts.square_tip_point + dest_x * dx + dest_y * dy)
            square_deltas = [ [0, 0], [1, 0], [1, 1], [0, 1] ]
            for move_pt, delta in zip(top_side.points, square_deltas):
                from_pt = anim.static_point(move_pt)
                dest_pt = tip_position + dx * delta[0] + dy * delta[1]
                animator.animate_value([from_pt, dest_pt, dest_pt], duration, anim.move_absolute_point(move_pt))
            animator.animate_value([0., 5.], short_duration, anim.change_thickness(top_side))

            hidden_sides = other_sides[cube_coord[0] + cube_x][cube_coord[1] + cube_y][cube_z]
            for side in hidden_sides:
                anim.anim_hide_item(animator, quick_reveal_duration, side)

    eq_offsets = [0, 2, 4, 7]
    for power_eq, offset in zip(geo.power_eqs, eq_offsets):
        from_pt = anim.static_point(power_eq[1].position)
        dest_pt = anim.static_point(pts.square_tip_point + anim.static_point(40., 0.) + offset * dx)
        animator.animate_value([from_pt, dest_pt, dest_pt], duration, anim.move_absolute_point(power_eq[1].position))
        
def make_triangle_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    destinations = _get_square_destinations()
    dx, dy = pts.square_deltas
    for which_cube, cube_coord, slice, dest_coord in destinations:
        cube_z = cube_coord[2]
        for cube_x, cube_y in product(range(slice[0]), range(slice[1])):
            dest_x = dest_coord[0] + cube_x
            dest_y = dest_coord[1] - cube_y

            max_dest = max(dest_x, dest_y)
            extra_x = (max_dest - dest_y) if dest_y < max_dest else 0
            extra_y = (max_dest - dest_x) if dest_x < max_dest else 0
            tip_position = anim.static_point(pts.square_tip_point + (dest_x + extra_x) * dx + (dest_y + extra_y) * dy)
            square_deltas = [ [0, 0], [1, 0], [1, 1], [0, 1] ]

            top_side = geo.top_sides[which_cube][cube_coord[0] + cube_x][cube_coord[1] + cube_y][cube_z]
            for move_pt, delta in zip(top_side.points, square_deltas):
                from_pt = anim.static_point(move_pt)
                dest_pt = tip_position + dx * delta[0] + dy * delta[1]
                animator.animate_value([from_pt, dest_pt, dest_pt], duration, anim.move_absolute_point(move_pt))
            animator.animate_value([0., 5.], short_duration, anim.change_thickness(top_side))

    eq_offsets = [0, 1, 3, 6]
    for power_eq, offset in zip(geo.power_eqs, eq_offsets):
        from_pt = anim.static_point(power_eq[1].position)
        dest_pt = anim.static_point(pts.square_tip_point + anim.static_point(60., 40.) + offset * 2 * dx)
        animator.animate_value([from_pt, dest_pt, dest_pt], duration, anim.move_absolute_point(power_eq[1].position))
        
def prepare_to_add_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    min_pt, max_pt = anim.min_max(anim.flatten([top_side.get_all_points() for top_side in anim.flatten(geo.top_sides[-1])]))
    rect_distance = 50.
    rect_width = 30.
    rect_spacing = 10.
    eq_distance = 100.

    for top_sides, right_rect in zip(geo.top_sides, geo.right_rects):
        for top_side in anim.flatten(top_sides):
            center = anim.center_of(top_side.points)
            for move_pt  in top_side.points:
                animator.animate_value([0., anim.qpi], duration, anim.rotate_absolute_point_around(move_pt, center))

        cube_min_pt, cube_max_pt = anim.min_max(anim.flatten([top_side.get_all_points() for top_side in anim.flatten(top_sides)]))

        right_rect.p1.set_absolute_point(anim.point(max_pt.x() + rect_distance,              cube_min_pt.y() + rect_spacing))
        right_rect.p2.set_absolute_point(anim.point(max_pt.x() + rect_distance + rect_width, cube_min_pt.y() + rect_spacing * 2))
        anim.anim_reveal_item(animator, quick_reveal_duration, right_rect)
        from_pt = anim.static_point(right_rect.p2)
        dest_pt = anim.static_point(right_rect.p2.x(), cube_max_pt.y() - rect_spacing)
        animator.animate_value([from_pt, dest_pt, dest_pt], short_duration, anim.move_absolute_point(right_rect.p2))

    for power_eq in geo.power_eqs:
        from_pt = anim.static_point(power_eq[1].position)
        dest_pt = anim.static_point(max_pt.x() + eq_distance, from_pt.y())
        animator.animate_value([from_pt, dest_pt, dest_pt], duration, anim.move_absolute_point(power_eq[1].position))
        


#################################################################
#
# Animation

nicomachu_sums = anim.simple_animation.from_module(globals())
