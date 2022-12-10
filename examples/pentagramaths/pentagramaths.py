import anim
from typing import List as _List

#################################################################
#
# Description

name = 'Pentagramaths'
description = 'Mathologer video: https://www.youtube.com/watch?v=w4AUOgfW9NI'
loop = False
reset_on_change = True
has_pointing_arrow = False


#################################################################
#
# Options

branches_count = anim.option('Number of branches', 'The number of branches the star will have', '5', ['5', '7', '9', '11'])

def count() -> int:
    return int(branches_count.value)

def skip() -> int:
    return count() // 2

def reset(animation: anim.animation, scene: anim.scene, animator: anim.animator):
    animation.current_shot_index = -1

def other(which: int, offset: int = 1) -> int:
    return (which + count() + offset) % count()


#################################################################
#
# Points and geometries

class points(anim.points):
    def __init__(self):
        super().__init__()

        self._gen_tips()

    def _gen_tips(self):
        self.tips = anim.create_points_around_origin(300., count(), 0.2352)

pts: points = None


#################################################################
#
# Points and geometries

class geometries(anim.geometries):
    def __init__(self, pts: points):
        super().__init__(False)

        self.colors = [
            anim.orange, anim.red, anim.purple, anim.cyan, anim.blue, anim.green,
            anim.dark_orange, anim.dark_red, anim.dark_purple, anim.dark_cyan, anim.dark_blue, anim.dark_green
        ]

        self._gen_lines(pts)
        self._gen_crossings()
        self._gen_triangles(pts)
        self._gen_branches()
        self._gen_dots()

    def _gen_lines(self, pts: points):
        count = len(pts.tips)
        self.lines = [anim.line(pts.tips[i], pts.tips[other(i, skip())]).thickness(2.) for i in range(count)]

    def _gen_crossings(self):
        count = len(self.lines)
        self.crossings = [
            (
                anim.two_lines_any_intersection(self.lines[other(i,  0     )], self.lines[other(i, -1)]),
                anim.two_lines_any_intersection(self.lines[other(i, -skip())], self.lines[other(i, -1)]),
            ) for i in range(count)]

    def _gen_triangles(self, pts: points):
        count = len(self.crossings)
        triangle_tips = [anim.point(tip) for tip in pts.tips]
        self.triangles = [(
            triangle_tips[i], 
            self.crossings[i][0],
            self.crossings[i][1],
        ) for i in range(count)]

    def _gen_branches(self):
        count = len(self.triangles)
        self.branches = [
            anim.polygon(self.triangles[i]).fill(self.colors[i]).outline(anim.black).thickness(1.)
            for i in range(count)
        ]

    def _gen_dots(self):
        self.dots = [anim.circle(anim.point(branch.center()), 5.).fill(anim.black) for branch in self.branches]

geo: geometries = None


#################################################################
#
# Actors

def generate_actors(animation: anim.animation, scene: anim.scene):
    global pts; pts = points()
    global geo; geo = geometries(pts)

    actors = [
        [anim.actor('Line', '', line) for line in geo.lines],
        [anim.actor('Branch', '', branch) for branch in geo.branches],
        [anim.actor('Dot', '', dot) for dot in geo.dots],
    ]
    animation.add_actors(actors, scene)
    scene.add_item(anim.create_invisible_rect(-600, -600, 1200, 1200))


#################################################################
#
# Prepare animation

def prepare_playing(animation: anim.animation, scene: anim.scene, animator: anim.animator):
    geo.reset()


#################################################################
#
# Shots

duration = 1.

def generate_shots(animation: anim.animation):
    def rotate_star_to_horizontal_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
        angle = anim.line_angle(geo.lines[- (skip() // 2)])
        center = anim.center_of(pts.tips)
        dot_points = [dot.center for dot in geo.dots]
        for pt in anim.flatten([pts.tips, geo.crossings, geo.triangles, dot_points]):
            animator.animate_value([0., -angle], duration, anim.rotate_point_around(pt, center))
    animation.add_shots(anim.shot('', '', rotate_star_to_horizontal_shot))

    for which in range(1, skip()+1):
        if which <= skip() // 2:
            _gen_slide_duo(which, animation)
        else:
            _gen_flip_duo(which, animation)

def _gen_flip_duo(which: int, animation: anim.animation):
    def flip_left_branch_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
        tip = anim.static_point(geo.triangles[which][0])
        for pt in anim.flatten([geo.triangles[which], geo.dots[which].center]):
            animator.animate_value([0., anim.pi], duration, anim.rotate_point_around(pt, tip))
    animation.add_shots(anim.shot('', '', flip_left_branch_shot))

    def flip_right_branch_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
        tip = anim.static_point(geo.triangles[-which][0])
        for pt in anim.flatten([geo.triangles[-which], geo.dots[-which].center]):
            animator.animate_value([0., anim.pi], duration, anim.rotate_point_around(pt, tip))
    animation.add_shots(anim.shot('', '', flip_right_branch_shot))

    def move_both_branches_to_top_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
        delta = geo.triangles[0][0] - geo.triangles[which][0]
        for pt in anim.flatten([geo.triangles[which], geo.dots[which].center]):
            animator.animate_value([anim.static_point(pt), anim.static_point(pt + delta)], duration, anim.move_point(pt))
        delta = geo.triangles[0][0] - geo.triangles[-which][0]
        for pt in anim.flatten([geo.triangles[-which], geo.dots[-which].center]):
            animator.animate_value([anim.static_point(pt), anim.static_point(pt + delta)], duration, anim.move_point(pt))
    animation.add_shots(anim.shot('', '', move_both_branches_to_top_shot))

def _gen_slide_duo(which: int, animation: anim.animation):
    def move_first_branch_to_crossing_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
        delta = geo.crossings[0][1] - geo.triangles[which][0]
        for pt in anim.flatten([geo.triangles[which], geo.dots[which].center]):
            animator.animate_value([anim.static_point(pt), anim.static_point(pt + delta)], duration, anim.move_point(pt))
    animation.add_shots(anim.shot('', '', move_first_branch_to_crossing_shot))

    def move_last_branch_to_crossing_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
        delta = geo.crossings[0][0] - geo.triangles[-which][0]
        for pt in anim.flatten([geo.triangles[-which], geo.dots[-which].center]):
            animator.animate_value([anim.static_point(pt), anim.static_point(pt + delta)], duration, anim.move_point(pt))
    animation.add_shots(anim.shot('', '', move_last_branch_to_crossing_shot))

    def move_first_branch_to_top_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
        delta = geo.triangles[0][0] - geo.crossings[0][1]
        for pt in anim.flatten([geo.triangles[which], geo.dots[which].center]):
            animator.animate_value([anim.static_point(pt), anim.static_point(pt + delta)], duration, anim.move_point(pt))
    animation.add_shots(anim.shot('', '', move_first_branch_to_top_shot))

    def move_last_branch_to_top_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
        delta = geo.triangles[0][0] - geo.crossings[0][0]
        for pt in anim.flatten([geo.triangles[-which], geo.dots[-which].center]):
            animator.animate_value([anim.static_point(pt), anim.static_point(pt + delta)], duration, anim.move_point(pt))
    animation.add_shots(anim.shot('', '',move_last_branch_to_top_shot))


#################################################################
#
# Animation

pentagramaths = anim.simple_animation.from_module(globals())
