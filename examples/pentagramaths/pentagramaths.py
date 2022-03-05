import anim

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


#################################################################
#
# Points and geometries

tips = []
lines = []
crossings = []
triangles = []
branches = []
dots = []
colors = [
    anim.orange, anim.red, anim.purple, anim.cyan, anim.blue, anim.green,
    anim.dark_orange, anim.dark_red, anim.dark_purple, anim.dark_cyan, anim.dark_blue, anim.dark_green
]

def other(which: int, offset: int = 1) -> int:
    return (which + count() + offset) % count()

def _gen_tips():
    global tips
    tips = anim.create_points_around_origin(300., count(), 0.2352)

def _gen_lines():
    global lines
    count = len(tips)
    lines = [anim.line(tips[i], tips[other(i, skip())]).thickness(2.) for i in range(count)]

def _gen_crossings():
    global crossings
    count = len(lines)
    crossings = [(
        anim.two_lines_any_intersection(lines[other(i,  0)], lines[other(i, -1)]),
        anim.two_lines_any_intersection(lines[other(i, -skip())], lines[other(i, -1)]),
    ) for i in range(count)]

def _gen_triangles():
    global triangles
    count = len(crossings)
    triangle_tips = [anim.point(tip) for tip in tips]
    triangles = [(
        triangle_tips[i], 
        crossings[i][0],
        crossings[i][1],
    ) for i in range(count)]

def _gen_branches():
    global branches
    count = len(triangles)
    branches = [
        anim.polygon(triangles[i]).fill(colors[i]).outline(anim.black).thickness(1.)
        for i in range(count)
    ]

def _gen_dots():
    global dots
    dots = [anim.circle(anim.point(branch.center()), 5.).fill(anim.black) for branch in branches]


#################################################################
#
# Actors

def generate_actors(animation: anim.animation, scene: anim.scene):
    _gen_tips()
    _gen_lines()
    _gen_crossings()
    _gen_triangles()
    _gen_branches()
    _gen_dots()

    actors = [
        [anim.actor('Line', '', line) for line in lines],
        [anim.actor('Branch', '', branch) for branch in branches],
        [anim.actor('Dot', '', dot) for dot in dots],
    ]
    animation.add_actors(actors, scene)
    scene.add_item(anim.create_invisible_rect(-600, -600, 1200, 1200))


#################################################################
#
# Prepare animation

def prepare_playing(animation: anim.animation, scene: anim.scene, animator: anim.animator):
    for pt in anim.find_all_of_type(globals(), anim.point):
        pt.reset()
    for poly in anim.find_all_of_type(globals(), anim.polygon):
        for pt in poly.get_all_points():
            pt.reset()
    for dot in dots:
        dot.center.reset()


#################################################################
#
# Shots

duration = 1.

def generate_shots(animation: anim.animation):
    def rotate_star_to_horizontal_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
        angle = anim.line_angle(lines[- (skip() // 2)]) * 180. / anim.math.pi
        center = anim.center_of(tips)
        dot_points = [dot.center for dot in dots]
        for pt in anim.flatten([tips, crossings, triangles, dot_points]):
            animator.animate_value([0., -angle], duration, anim.rotate_point_around(pt, center))
    animation.add_shots(anim.shot('', '', rotate_star_to_horizontal_shot))

    for which in range(1, skip()+1):
        if which <= skip() // 2:
            _gen_slide_duo(which, animation)
        else:
            _gen_flip_duo(which, animation)

def _gen_flip_duo(which: int, animation: anim.animation):
    def flip_left_branch_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
        tip = anim.static_point(triangles[which][0])
        for pt in anim.flatten([triangles[which], dots[which].center]):
            animator.animate_value([0., 180.], duration, anim.rotate_point_around(pt, tip))
    animation.add_shots(anim.shot('', '', flip_left_branch_shot))

    def flip_right_branch_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
        tip = anim.static_point(triangles[-which][0])
        for pt in anim.flatten([triangles[-which], dots[-which].center]):
            animator.animate_value([0., 180.], duration, anim.rotate_point_around(pt, tip))
    animation.add_shots(anim.shot('', '', flip_right_branch_shot))

    def move_both_branches_to_top_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
        delta = triangles[0][0] - triangles[which][0]
        for pt in anim.flatten([triangles[which], dots[which].center]):
            animator.animate_value([anim.static_point(pt), anim.static_point(pt + delta)], duration, anim.move_point(pt))
        delta = triangles[0][0] - triangles[-which][0]
        for pt in anim.flatten([triangles[-which], dots[-which].center]):
            animator.animate_value([anim.static_point(pt), anim.static_point(pt + delta)], duration, anim.move_point(pt))
    animation.add_shots(anim.shot('', '', move_both_branches_to_top_shot))

def _gen_slide_duo(which: int, animation: anim.animation):
    def move_first_branch_to_crossing_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
        delta = crossings[0][1] - triangles[which][0]
        for pt in anim.flatten([triangles[which], dots[which].center]):
            animator.animate_value([anim.static_point(pt), anim.static_point(pt + delta)], duration, anim.move_point(pt))
    animation.add_shots(anim.shot('', '', move_first_branch_to_crossing_shot))

    def move_last_branch_to_crossing_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
        delta = crossings[0][0] - triangles[-which][0]
        for pt in anim.flatten([triangles[-which], dots[-which].center]):
            animator.animate_value([anim.static_point(pt), anim.static_point(pt + delta)], duration, anim.move_point(pt))
    animation.add_shots(anim.shot('', '', move_last_branch_to_crossing_shot))

    def move_first_branch_to_top_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
        delta = triangles[0][0] - crossings[0][1]
        for pt in anim.flatten([triangles[which], dots[which].center]):
            animator.animate_value([anim.static_point(pt), anim.static_point(pt + delta)], duration, anim.move_point(pt))
    animation.add_shots(anim.shot('', '', move_first_branch_to_top_shot))

    def move_last_branch_to_top_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
        delta = triangles[0][0] - crossings[0][0]
        for pt in anim.flatten([triangles[-which], dots[-which].center]):
            animator.animate_value([anim.static_point(pt), anim.static_point(pt + delta)], duration, anim.move_point(pt))
    animation.add_shots(anim.shot('', '',move_last_branch_to_top_shot))


#################################################################
#
# Animation

pentagramaths = anim.simple_animation.from_module(globals())
