import anim


#################################################################
#
# Description

name = 'Three Bisectors Meet'
description = 'Mathologer video: https://www.youtube.com/watch?v=XOS73mTomPY'
loop = False
reset_on_change = False
has_pointing_arrow = False


#################################################################
#
# Points and geometries

def other1(which: int):
    return (which + 1) % 3

def other2(which: int):
    return (which + 2) % 3

corners = [anim.point(0., 0.), anim.point(1000., -300.), anim.point(400., 200.)]
lengths = [
    (
        anim.two_points_distance(corners[i], corners[other1(i)]),
        anim.two_points_distance(corners[i], corners[other2(i)])
    )
    for i in range(3)
]
colors = [anim.red, anim.green, anim.blue]

corner_angles = [
    anim.polygon([
        corners[i],
        anim.two_points_convex_sum(corners[i], corners[other1(i)], 50. / lengths[i][0]),
        anim.two_points_convex_sum(corners[i], corners[other2(i)], 50. / lengths[i][1])
    ]).fill(colors[i]).outline(anim.no_color).thickness(0.)
    for i in range(3)
]

bisectors_points = [
    anim.four_points_bisector(corners[i], corners[other1(i)], corners[i], corners[other2(i)])
    for i in range(3)
]

center = anim.four_points_any_intersection(*bisectors_points[0], *bisectors_points[1])

bisectors = [
    anim.line(corners[i], anim.point(center))
    for i in range(3)
]

radius_points = [
    anim.point_to_two_points_projection(center, corners[other1(i)], corners[other2(i)])
    for i in range(3)
]

radii = [
    anim.line(radius_points[i], center)
    for i in range(3)
]

triangle = anim.polygon(corners).fill(anim.no_color).outline(anim.black).thickness(2.)
circle = anim.radius_circle(center, radius_points[0]).fill(anim.orange).outline(anim.no_color).set_opacity(0.5)
circle_center = anim.circle(center, 10.).fill(anim.red).outline(anim.no_color)
circle_radius = [
    anim.circle(pt, 6.).fill(co).outline(anim.no_color) for pt, co in zip(radius_points, colors)
]

def _prepare_anim():
    circle.set_opacity(0.)
    circle.fill(anim.orange)
    circle_center.set_opacity(0.)
    for cr in circle_radius:
        cr.set_opacity(0.)
    for b in bisectors:
        b.set_opacity(0.)
    triangle.set_opacity(0.)
    for ca in corner_angles:
        ca.set_opacity(0.)
    for r in radii:
        r.set_opacity(0.)
    for rp in radius_points:
        rp.reset()

def _move_between_points(which: int, back: bool, animator: anim.animator):
    cor = corners[which]
    circle.set_radius(radius_points[(which + 1) % 3])
    hues = [anim.orange, colors[which]]
    if back:
        hues.reverse()
    animator.animate_value(hues, duration, anim.change_fill_color(circle))
    move = [anim.static_point(center.original_point), anim.static_point(cor)]
    if back:
        move.reverse()
    animator.animate_value(move, duration, anim.move_point(center))
    for i in range(2):
        other = (which + 1 + i) % 3
        move = [anim.static_point(radius_points[other].original_point), anim.static_point(cor)]
        if back:
            move.reverse()
        animator.animate_value(move, duration, anim.move_point(radius_points[other]))

def _prepare_radii(which: int, animator: anim.animator):
    for i in range(3):
        # Note: avoid extending or retracting a line that is already in that position.
        if which == 0 and i == 0:
            continue
        if which == 1 and i == 2:
            continue
        if which == 2 and i == 0:
            continue
        r = radii[i]
        opacities = [0., 1.]
        move = [anim.static_point(center), anim.static_point(r.p1.original_point)]
        if i == which:
            opacities.reverse()
            move.reverse()
        animator.animate_value(opacities, duration, anim.reveal_item(r))
        animator.animate_value(move, duration, anim.move_point(r.p1))


#################################################################
#
# Actors

actors = [
    anim.actor('Triangle', '', triangle),
    anim.actor('Circle', '', circle),
    anim.actor('Center', '', circle_center),
    [ anim.actor('Angle', '', angle) for angle in corner_angles],
    [ anim.actor('Touch point', '', r) for r in circle_radius],
    [ anim.actor('Radius', '', r) for r in radii],
    [ anim.actor('Bisector', '', bisector) for bisector in bisectors ],
]


#################################################################
#
# Shots

duration = 1.

def show_triangle_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''Arbitrary Triangle'''
    _prepare_anim()
    animator.animate_value([0., 1.], duration, anim.reveal_item(triangle))

def show_angles_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''Arbitrary Triangle'''
    for ca in corner_angles:
        animator.animate_value([0., 1.], duration, anim.reveal_item(ca))

def grow_bisectors_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''Why do they meet at a single point?'''
    for i in range(3):
        bisectors[i].p2.set_point(corners[i])
        bisectors[i].set_opacity(1.)
        animator.animate_value([
            anim.static_point(corners[i]),
            anim.static_point(bisectors[i].p2.original_point)], duration, anim.move_point(bisectors[i].p2))
    animator.animate_value([0., 0., 0., 1.], duration, anim.reveal_item(circle_center))

def show_circle_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''Why do they meet at a single point?'''
    animator.animate_value([0., 1.], duration, anim.reveal_item(circle))
    for cr in circle_radius:
        animator.animate_value([0., 0., 1.], duration, anim.reveal_item(cr))

def prepare_radii_0_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''Why do they meet at a single point?'''
    _prepare_radii(0, animator)

def move_to_corner_0_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''Why do they meet at a single point?'''
    return _move_between_points(0, False, animator)

def move_to_center_0_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''Why do they meet at a single point?'''
    return _move_between_points(0, True, animator)

def prepare_radii_1_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''Why do they meet at a single point?'''
    _prepare_radii(1, animator)

def move_to_corner_1_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''Why do they meet at a single point?'''
    return _move_between_points(1, False, animator)

def move_to_center_1_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''Why do they meet at a single point?'''
    return _move_between_points(1, True, animator)

def prepare_radii_2_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''Why do they meet at a single point?'''
    _prepare_radii(2, animator)

def move_to_corner_2_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''Why do they meet at a single point?'''
    return _move_between_points(2, False, animator)

def move_to_center_2_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    '''Why do they meet at a single point?'''
    return _move_between_points(2, True, animator)

def show_circle_again_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    ''':)'''
    circle.set_radius(radius_points[0])
    cen = anim.static_point(center)
    for i in range(3):
        radii[i].set_opacity(0.)
        rad = anim.static_point(radius_points[i].original_point)
        animator.animate_value([rad, cen, rad, cen], duration * 4, anim.move_point(radius_points[i]))


#################################################################
#
# Animation

animation = anim.simple_animation.from_module(globals())
