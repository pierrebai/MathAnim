import anim

from typing import List as _List

#################################################################
#
# Description

name = 'Pythagora with Three triangles'
description = 'Mathologer video: https://www.youtube.com/watch?v=r4gOlttnJ_E'
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
        short_side = 600.
        long_side  = 800.
        corner_side = 60.

        corners = [anim.point(0., 0.), anim.point(0., long_side), anim.point(short_side, long_side)]
        angle = anim.horizontal_angle(corners[2], corners[0])

        self.main_corners  = [anim.point(anim.trf.rotate_around_origin(pt, angle)) for pt in corners]
        self.left_corners  = [anim.point(pt) for pt in self.main_corners]
        self.right_corners = [anim.point(pt) for pt in self.main_corners]

        self.angle_corners = [
            anim.point(0.,          long_side),
            anim.point(0.,          long_side - corner_side),
            anim.point(corner_side, long_side - corner_side),
            anim.point(corner_side, long_side)]

        self.angle_corners = [anim.point(anim.trf.rotate_around_origin(pt, angle)) for pt in self.angle_corners]

pts: points = points()


#################################################################
#
# Geometries

class geometries(anim.geometries):
    label_size = 50.

    def __init__(self, pts: points):
        super().__init__()
        self.main_triangle  = anim.polygon(pts.main_corners ).thickness(0.).outline(anim.black).fill(anim.red)
        self.left_triangle  = anim.polygon(pts.left_corners ).thickness(0.).outline(anim.black).fill(anim.red)
        self.right_triangle = anim.polygon(pts.right_corners).thickness(0.).outline(anim.black).fill(anim.red)

        dlt = geometries.label_size / 2
        dlt2 = dlt * 2.
        dlt3 = dlt * 3.
        dlt4 = dlt * 4.

        self.main_side_labels  = geometries._create_tri_side_labels(self.main_triangle,
            [anim.static_point(dlt, -dlt3), anim.static_point(-dlt4, -dlt2), anim.static_point(-dlt2, 0.)])
        self.left_side_labels  = geometries._create_tri_side_labels(self.left_triangle,
            [anim.static_point(-dlt4, -dlt2), anim.static_point(-dlt2, -dlt3), anim.static_point(dlt2, -dlt)])
        self.right_side_labels = geometries._create_tri_side_labels(self.right_triangle,
            [anim.static_point(0., -dlt3), anim.static_point(dlt2, 0.), anim.static_point(-dlt2, 0.)])

        self.main_scale_labels  = geometries._create_tri_scale_labels(self.main_triangle,  'C')
        self.left_scale_labels  = geometries._create_tri_scale_labels(self.left_triangle,  'A')
        self.right_scale_labels = geometries._create_tri_scale_labels(self.right_triangle, 'B')

        self.main_power_label  = geometries._create_tri_power_label(self.main_scale_labels[2])
        self.left_power_label  = geometries._create_tri_power_label(self.left_scale_labels[1])
        self.right_power_label = geometries._create_tri_power_label(self.right_scale_labels[0])

        self.right_angle = anim.polygon(pts.angle_corners).fill(anim.black).outline(anim.no_color)

        self.left_to_main_arrow = anim.create_pointing_arrow(
            self.left_scale_labels[2].position,
            self.main_scale_labels[1].position, anim.pale_blue)

        self.right_to_main_arrow = anim.create_pointing_arrow(
            self.right_scale_labels[2].position,
            self.main_scale_labels[0].position, anim.pale_blue)

        self.background_rect = self.create_background_rect(pts, anim.point(0.3, 0.57), anim.point(0.3, 0.15))

        self._order_items()

    def _order_items(self):
        self.main_triangle.set_z_order(1.)
        self.right_angle.set_z_order(2.)
        for label in anim.find_all_of_type(self.__dict__, anim.scaling_text):
            label.set_z_order(3.)

    @staticmethod
    def _relative_mid_point(points: _List[anim.point]) -> anim.selected_point:
        return anim.selected_point(points, lambda points: anim.weighted_center_of(points))

    @staticmethod
    def _create_tri_label(label: str, pos: anim.point, font_size: float = label_size) -> anim.scaling_text:
        return anim.create_sans_bold_text(label, pos, font_size).fill(anim.black)

    @staticmethod
    def _create_tri_side_label(tri: anim.polygon, s1: int, s2: int, label: str, offset: anim.static_point) -> anim.scaling_text:
        p1, p2 = tri.points[s1], tri.points[s2]
        pos = geometries._relative_mid_point([p1, p2])
        pos = anim.relative_point(pos, offset)
        angle = anim.two_points_angle(p1, p2) + anim.hpi
        return geometries._create_tri_label(label, pos)

    @staticmethod
    def _create_tri_side_labels(tri: anim.polygon, offsets: _List[anim.static_point]) -> _List[anim.scaling_text]:
        return [
            geometries._create_tri_side_label(tri, 0, 1, 'B', offsets[0]),
            geometries._create_tri_side_label(tri, 1, 2, 'A', offsets[1]),
            geometries._create_tri_side_label(tri, 2, 0, 'C', offsets[2]),
        ]

    @staticmethod
    def _create_tri_scale_label(tri: anim.polygon, label: str) -> anim.scaling_text:
        pos = geometries._relative_mid_point(tri.points)
        return geometries._create_tri_label(label, pos)

    @staticmethod
    def _create_tri_scale_labels(tri: anim.polygon, label: str) -> _List[anim.scaling_text]:
        return [
            geometries._create_tri_scale_label(tri, label),
            geometries._create_tri_scale_label(tri, label),
            geometries._create_tri_scale_label(tri, label),
        ]

    @staticmethod
    def _create_tri_power_label(scale_label: anim.scaling_text) -> anim.scaling_text:
        pos = anim.relative_point(scale_label.exponent_pos())
        return geometries._create_tri_label('2', pos, geometries.label_size * 0.6)


geo: geometries = geometries(pts)


#################################################################
#
# Actors

actors = [
    anim.actor('Triangle', '', geo.main_triangle),
    anim.actor('Triangle', '', geo.left_triangle),
    anim.actor('Triangle', '', geo.right_triangle),
    anim.actor('Right Angle', '', geo.right_angle),
    anim.actor('Background', '', geo.background_rect),
    [anim.actor('Label', '', label) for label in geo.main_side_labels],
    [anim.actor('Label', '', label) for label in geo.right_side_labels],
    [anim.actor('Label', '', label) for label in geo.left_side_labels],
    [anim.actor('Label', '', label) for label in geo.main_scale_labels],
    [anim.actor('Label', '', label) for label in geo.right_scale_labels],
    [anim.actor('Label', '', label) for label in geo.left_scale_labels],
    anim.actor('Label', '', geo.main_power_label),
    anim.actor('Label', '', geo.right_power_label),
    anim.actor('Label', '', geo.left_power_label),
    anim.actor('Arrow', '', geo.left_to_main_arrow),
    anim.actor('Arrow', '', geo.right_to_main_arrow),
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
    Right Triangle
    '''
    #geo.background_rect.set_opacity(1.)
    anim.anim_reveal_item(animator, duration, geo.right_angle)
    anim.anim_reveal_item(animator, duration, geo.main_triangle)
    for label in geo.main_side_labels:
        anim.anim_reveal_item(animator, duration, label)

def create_copies_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Make two copies
    '''
    triangles    = [
        geo.left_triangle,
        geo.right_triangle,
    ]
    angles  = [
        anim.vertical_angle(geo.left_triangle.points[0], geo.left_triangle.points[1]),
        anim.vertical_angle(geo.right_triangle.points[1], geo.right_triangle.points[2]),
    ]
    centers = [
        geo.left_triangle.points[0],
        geo.right_triangle.points[2],
    ]
    anim.anim_hide_item(animator, short_duration, geo.right_angle)
    for tri, angle, center in zip(triangles, angles, centers):
        anim.anim_reveal_item(animator, quick_reveal_duration, tri)
        for pt in tri.points:
            animator.animate_value([0., angle], short_duration, anim.rotate_point_around(pt, center))
    for label in geo.right_side_labels:
        anim.anim_reveal_item(animator, short_duration, label)
    for label in geo.left_side_labels:
        anim.anim_reveal_item(animator, short_duration, label)

def flip_copies_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Make two copies
    '''
    triangles    = [
        geo.left_triangle,
        geo.right_triangle,
    ]
    horiz_mid = anim.mid_point(geo.main_triangle.points[0], geo.main_triangle.points[2])
    mirror_line = anim.line(anim.point(horiz_mid.x(), 1.), anim.point(horiz_mid.x(), -1.))
    for tri in triangles:
        for pt in tri.points:
            animator.animate_value([0., 1.], short_duration, anim.move_point_to_line_mirror(pt, mirror_line))

def move_copies_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Make two copies
    '''
    triangles    = [
        geo.left_triangle,
        geo.right_triangle,
    ]
    move_delta = anim.point.distance(geo.main_triangle.points[1], geo.main_triangle.points[2]) / 4.
    moves = [
        anim.static_point(-move_delta, -move_delta),
        anim.static_point( move_delta, -move_delta),
    ]
    for tri, move in zip(triangles, moves):
        for pt in tri.points:
            from_pt = anim.static_point(pt)
            dest_pt = pt + move
            animator.animate_value([from_pt, dest_pt], short_duration, anim.move_point(pt))

def _animate_triangle_scale(tri: anim.polygon, scale_factor: float, animator: anim.animator):
    angle_pt = tri.points[1]
    pt = tri.points[2]
    from_pt = anim.static_point(pt)
    dest_pt = anim.static_point(anim.two_points_convex_sum(angle_pt, pt, scale_factor))
    animator.animate_value([from_pt, dest_pt], duration, anim.move_absolute_point(pt))

    pt = tri.points[0]
    from_pt = anim.static_point(pt)
    dest_pt = anim.static_point(anim.two_points_convex_sum(angle_pt, pt, scale_factor))
    animator.animate_value([from_pt, dest_pt], duration, anim.move_absolute_point(pt))

def _animate_triangle_scale_labels(side_labels, scale_labels, animator: anim.animator):
    for side, scale in zip(side_labels, scale_labels):
        from_pt = anim.static_point(scale.position)
        dest_pt = anim.static_point(side.exponent_pos())
        anim.anim_reveal_item(animator, short_duration, scale)
        animator.animate_value([from_pt, from_pt, dest_pt], duration, anim.move_absolute_point(scale.position))

def scale_left_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Scale the left triangle by a factor of A ...
    '''
    tri = geo.left_triangle
    p0, p1, p2 = tri.points
    scale_factor = 1.1 * anim.point.distance(p1, p2) / anim.point.distance(p0, p2)
    _animate_triangle_scale(tri, scale_factor, animator)

def scale_left_labels_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Scale the left triangle by a factor of A ...
    '''
    _animate_triangle_scale_labels(geo.left_side_labels, geo.left_scale_labels, animator)

def scale_right_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Scale the right triangle by a factor of B ...
    '''
    tri = geo.right_triangle
    p0, p1, p2 = tri.points
    scale_factor = 1.1 * anim.point.distance(p1, p0) / anim.point.distance(p0, p2)
    _animate_triangle_scale(tri, scale_factor, animator)

def scale_right_labels_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Scale the right triangle by a factor of B ...
    '''
    _animate_triangle_scale_labels(geo.right_side_labels, geo.right_scale_labels, animator)

def scale_main_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    ... scale the last triangle by a factor of C
    '''
    scale_factor = 1.1
    _animate_triangle_scale(geo.main_triangle, scale_factor, animator)

def scale_main_labels_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    ... scale the last triangle by a factor of C
    '''
    _animate_triangle_scale_labels(geo.main_side_labels, geo.main_scale_labels, animator)

def corresponding_sides_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Now comes the magic
    '''
    anim.anim_reveal_item(animator, duration, geo.left_to_main_arrow)
    anim.anim_reveal_item(animator, long_duration, geo.right_to_main_arrow)

def bring_together_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Can you see it?
    '''
    together_pt = anim.static_point(geo.main_triangle.points[1] - anim.static_point(0., 300.))
    dest_corners = [1, 2, 0]
    triangles = [geo.main_triangle, geo.left_triangle, geo.right_triangle]
    for tri, corner in zip(triangles, dest_corners):
        delta = anim.static_point(tri.points[corner] - together_pt)
        for pt in tri.points:
            from_pt = anim.static_point(pt)
            dest_pt = anim.static_point(pt - delta)
            animator.animate_value([from_pt, dest_pt, dest_pt, dest_pt], long_duration, anim.move_absolute_point(pt))
    
    anim.anim_hide_item(animator, quick_reveal_duration, geo.left_to_main_arrow)
    anim.anim_hide_item(animator, quick_reveal_duration, geo.right_to_main_arrow)

    hide_labels = [
        geo.main_side_labels  [0], geo.main_side_labels  [1],
        geo.main_scale_labels [0], geo.main_scale_labels [1],
        geo.left_side_labels  [0], geo.left_side_labels  [2],
        geo.left_scale_labels [0], geo.left_scale_labels [2],
        geo.right_side_labels [1], geo.right_side_labels [2],
        geo.right_scale_labels[1], geo.right_scale_labels[2],
    ]
    for label in hide_labels:
        anim.anim_hide_item(animator, short_duration, label)

def _animate_label_merge(moved_label: anim.scaling_text, dest_label: anim.scaling_text, power_label: anim.scaling_text, animator: anim.animator):
    from_pt = anim.static_point(moved_label.position)
    dest_pt = anim.static_point(dest_label.position)
    animator.animate_value([from_pt, dest_pt], short_duration, anim.move_absolute_point(moved_label.position))
    anim.anim_reveal_item(animator, duration, power_label)

def square_A_hint_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    A squared ...
    '''
    animator.animate_value([0., 0.], duration, lambda x: x)

def square_A_labels_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    ...
    '''
    _animate_label_merge(geo.left_side_labels [1], geo.left_scale_labels [1], geo.left_power_label, animator)

def square_B_hint_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    ... plus B squared ...
    '''
    animator.animate_value([0., 0.], duration, lambda x: x)

def square_B_labels_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    ...
    '''
    _animate_label_merge(geo.right_side_labels[0], geo.right_scale_labels[0], geo.right_power_label, animator)

def square_C_hint_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    ... equals C squared
    '''
    animator.animate_value([0., 0.], duration, lambda x: x)

def square_C_labels_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    ...
    '''
    _animate_label_merge(geo.main_side_labels[2], geo.main_scale_labels[2], geo.main_power_label, animator)

def final_equation_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    A² + B² = C²
    '''
    pass


#################################################################
#
# Animation

three_pythagora = anim.simple_animation.from_module(globals())
