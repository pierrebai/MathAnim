import anim


#################################################################
#
# Description

name = 'Pythagora with Three triangles'
description = 'Mathologer video: https://www.youtube.com/watch?v=r4gOlttnJ_E'
loop = False
reset_on_change = False
has_pointing_arrow = False

shot_duration = 2.
short_shot_duration = shot_duration / 3.

#################################################################
#
# Points

class points(anim.point):
    def __init__(self):
        super().__init__()
        corners = [anim.point(0., 0.), anim.point(0., 1200.), anim.point(500., 1200.)]
        angle = anim.horizontal_angle(corners[2], corners[0])
        self.main_corners = [anim.point(anim.trf.rotate_around_origin(pt, angle)) for pt in corners]
        self.right_corners = [anim.point(pt) for pt in self.main_corners]
        self.left_corners = [anim.point(pt) for pt in self.main_corners]

        self.angle_corners = [anim.point(0., 1200.), anim.point(0., 1140.), anim.point(60., 1140.), anim.point(60., 1200.)]
        self.angle_corners = [anim.point(anim.trf.rotate_around_origin(pt, angle)) for pt in self.angle_corners]

pts: points = points()


#################################################################
#
# Geometries

class geometries(anim.geometries):
    def __init__(self, pts):
        super().__init__()
        self.main_triangle  = anim.polygon(pts.main_corners ).thickness(0.).outline(anim.black).fill(anim.red)
        self.left_triangle = anim.polygon(pts.left_corners).thickness(0.).outline(anim.black).fill(anim.red)
        self.right_triangle  = anim.polygon(pts.right_corners ).thickness(0.).outline(anim.black).fill(anim.red)

        self.right_angle = anim.polygon(pts.angle_corners).fill(anim.black).outline(anim.no_color)

        min_pt, max_pt = anim.min_max(self.main_triangle.points + self.left_triangle.points + self.right_triangle.points)
        delta = max_pt - min_pt
        delta = max(delta.x(), delta.y())
        p1 = anim.point(min_pt - anim.static_point(delta * 0.4, delta * 0.9))
        p2 = anim.point(max_pt + anim.static_point(delta * 0.4, delta * 0.1))
        self.background_rect = anim.rectangle(p1, p2).outline(anim.gray).thickness(5.).fill(anim.no_color)

        def relative_mid_point(p1, p2):
            return anim.selected_point([p1, p2], lambda points: anim.mid_point(*points))

        def tri_side_label(tri, s1, s2, label):
            return anim.scaling_text(label, relative_mid_point(tri.points[s1], tri.points[s2]), 100.).fill(anim.black)

        self.main_labels = [
            tri_side_label(self.main_triangle, 0, 1, 'A'),
            tri_side_label(self.main_triangle, 1, 2, 'B'),
            tri_side_label(self.main_triangle, 2, 0, 'C'),
        ]

        self.left_labels = [
            tri_side_label(self.left_triangle, 0, 1, 'A'),
            tri_side_label(self.left_triangle, 1, 2, 'B'),
            tri_side_label(self.left_triangle, 2, 0, 'C'),
        ]

        self.right_labels = [
            tri_side_label(self.right_triangle, 0, 1, 'A'),
            tri_side_label(self.right_triangle, 1, 2, 'B'),
            tri_side_label(self.right_triangle, 2, 0, 'C'),
        ]

        self.main_triangle.setZValue(1.)
        self.right_angle.setZValue(2.)

        for label in anim.find_all_of_type(self.__dict__, anim.scaling_text):
            label.setZValue(3.)

geo: geometries = geometries(pts)


#################################################################
#
# Actors

actors = [
    anim.actor('Triangle', '', geo.main_triangle),
    anim.actor('Triangle', '', geo.right_triangle),
    anim.actor('Triangle', '', geo.left_triangle),
    anim.actor('Right Angle', '', geo.right_angle),
    anim.actor('Background', '', geo.background_rect),
    [anim.actor('Label', '', label) for label in geo.main_labels],
    [anim.actor('Label', '', label) for label in geo.left_labels],
    [anim.actor('Label', '', label) for label in geo.right_labels],
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
    geo.background_rect.set_opacity(1.)
    anim.anim_reveal_item(animator, shot_duration, geo.right_angle)
    anim.anim_reveal_item(animator, shot_duration, geo.main_triangle)
    for label in geo.main_labels:
        anim.anim_reveal_item(animator, shot_duration, label)

def make_copies_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Make two copies
    '''
    triangles    = [
        geo.left_triangle,
        geo.right_triangle,
    ]
    angles  = [
        anim.vertical_angle(geo.left_triangle.points[1], geo.left_triangle.points[2]),
        anim.vertical_angle(geo.right_triangle.points[0], geo.right_triangle.points[1]),
    ]
    centers = [
        geo.left_triangle.points[2],
        geo.right_triangle.points[0],
    ]
    anim.anim_hide_item(animator, short_shot_duration, geo.right_angle)
    for tri, angle, center in zip(triangles, angles, centers):
        anim.anim_reveal_item(animator, shot_duration / 8., tri)
        for pt in tri.points:
            animator.animate_value([0., angle], short_shot_duration, anim.rotate_point_around(pt, center))
    for label in geo.left_labels:
        anim.anim_reveal_item(animator, short_shot_duration, label)
    for label in geo.right_labels:
        anim.anim_reveal_item(animator, short_shot_duration, label)

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
            animator.animate_value([0., 1.], short_shot_duration, anim.move_point_to_line_mirror(pt, mirror_line))

def move_copies_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''
    Make two copies
    '''
    triangles    = [
        geo.left_triangle,
        geo.right_triangle,
    ]
    move_delta = anim.point.distance(geo.main_triangle.points[1], geo.main_triangle.points[2]) / 2.
    moves = [
        anim.static_point( move_delta, -move_delta),
        anim.static_point(-move_delta, -move_delta),
    ]
    for tri, move in zip(triangles, moves):
        for pt in tri.points:
            from_pt = anim.static_point(pt)
            dest_pt = pt + move
            animator.animate_value([from_pt, dest_pt], short_shot_duration, anim.move_point(pt))


#################################################################
#
# Animation

three_pythagora = anim.simple_animation.from_module(globals())
