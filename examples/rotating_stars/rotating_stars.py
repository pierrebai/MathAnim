import anim

import math

name = "Rotating Stars"
description = "Mathologer 3-4-7 Miracle: rotating interlinked polygons following a star trajectory."


#################################################################
#
# Options

sides_option = anim.option("Number of branches", "Number of branches on the star that the dots follows.", 7, 2, 20)
skip_option = anim.option("Star branch skip", "How many branches are skipped to go from one branch to the next.", 3, 1, 100)
ratio_option = anim.option("Percent of radius", "The position of the dots as a percentage of the radius of the circle they are on.", 90, 0, 100)

def sides():
    return sides_option.value

def skip():
    return min(skip_option.value, sides() - 1)

def inner_circle_ratio():
    return float(skip()) / float(sides())

def inner_count():
    return max(1, sides() - skip())

def dots_count():
    return skip()

def inner_circle_dot_ratio():
    return float(ratio_option.value) / 100.

def animation_speedup():
    return inner_count()

reveal_duration = 0.3


#################################################################
#
# Points

def _generate_points():
    global outer_center;   outer_center   = anim.point(0., 0.)
    global outer_radius;   outer_radius   = anim.outer_size
    global inner_radius;   inner_radius   = outer_radius * inner_circle_ratio()
    global inner_centers;  inner_centers  = anim.create_relative_points_around_center(outer_center, outer_radius - inner_radius, inner_count())
    global dot_radius;     dot_radius     = inner_radius * inner_circle_dot_ratio()
    global inner_dots_pos; inner_dots_pos = [anim.create_relative_points_around_center(center, dot_radius, skip()) for center in inner_centers]


#################################################################
#
# Actors

def generate_actors(animation: anim.animation, scene: anim.scene):
    _generate_points()

    global star;           star           = _gen_star(scene)
    global outer_circle;   outer_circle   = _gen_outer_circle(scene)
    global inner_circles;  inner_circles  = _gen_inner_circles(scene)
    global inner_dots;     inner_dots     = _gen_inner_dots(scene)
    global inner_polygons; inner_polygons = _gen_inner_polygons(scene)
    global inter_polygons; inter_polygons = _gen_inter_polygons(scene)

    animation.add_actors([outer_circle, inner_circles, inner_dots, inner_polygons, inter_polygons, star], scene)

def _gen_star(scene: anim.scene):
    pts = anim.create_roll_circle_in_circle_points(inner_radius, outer_radius, skip(), 240, inner_circle_dot_ratio())

    return anim.actor("star", "The star that the dots on the inner circle follow.",
        anim.create_polygon(pts).outline(anim.dark_gray))

def _gen_outer_circle(scene: anim.scene):
    return anim.actor("outer circle", "",
        anim.create_circle(outer_center, anim.outer_size).outline(anim.dark_blue).thickness(anim.line_width * 2))

def _gen_inner_circles(scene: anim.scene):
    return [anim.actor("inner circle", "", anim.create_disk(center, inner_radius)) for center in inner_centers]

def _gen_inner_dots(scene: anim.scene):
    return [
        [anim.actor("inner circle dot", "",
            anim.create_disk(dot, anim.dot_size).fill(anim.orange)) for dot in dots]
        for dots in inner_dots_pos]

def _gen_inner_polygons(scene: anim.scene):
    return [anim.actor("inner polygon", "",
        anim.create_polygon(dots).outline(anim.green))
        for dots in inner_dots_pos]

def _gen_inter_polygons(scene: anim.scene):
    outer_dots_pos = anim.transpose_lists(inner_dots_pos)
    return [anim.actor("outer polygon", "",
        anim.create_polygon(dots).outline(anim.blue))
        for dots in outer_dots_pos]


#################################################################
#
# Prepare animation

def prepare_playing(animation: anim.animation, scene: anim.scene, animator: anim.animator):
    for actor in animation.actors:
        actor.item.set_opacity(0)


#################################################################
#
# Reused animations

def _anim_inner_circle(which_inner: int, animator: anim.animator):
    animator.animate_value([0., 1.], reveal_duration, anim.reveal_item(inner_circles[which_inner]))

def _anim_other_inner_circle_dots(which_inner: int, which_dot: int, animator: anim.animator):
    animator.animate_value([0., 1.], reveal_duration, anim.reveal_item(inner_dots[which_inner][which_dot]))

def _anim_inner_circle_polygon(which_inner: int, animator: anim.animator):
    animator.animate_value([0., 1.], reveal_duration, anim.reveal_item(inner_polygons[which_inner]))

def _anim_inner_circle_polygon_arrow(which_inner: int, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    poly = inner_polygons[which_inner]
    animation.anim_pointing_arrow(poly.item.scene_rect().center(), reveal_duration / 2, scene, animator)


#################################################################
#
# Shots

def outer_circle_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Draw the outer circle

    This is the ounter circle
    insides which the smaller ones
    will rotate.
    """
    circle = outer_circle
    animator.animate_value([0., 1.], reveal_duration, anim.reveal_item(circle))
    animator.animate_value([0., 1.], reveal_duration, anim.reveal_item(scene.pointing_arrow))
    animation.anim_pointing_arrow(circle.item.scene_rect().center(), reveal_duration / 2, scene, animator)

def inner_circle_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Draw an inner circle

    This is one of the inner circle that
    rotates inside the outer circle.
    """
    _anim_inner_circle(0, animator)
    circle = inner_circles[0]
    animation.anim_pointing_arrow(circle.item.scene_rect().center(), reveal_duration / 2, scene, animator)

def inner_circle_dot_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Draw an inner-circle dot

    This dot on a circle is one
    of the corners of a polygon
    that will rotate, following
    the circle is it placed on.
    """
    dot = inner_dots[0][0]
    reveal = anim.reveal_item(dot)
    animator.animate_value([0., 1.], reveal_duration, reveal)
    animation.anim_pointing_arrow(dot.item.scene_rect().center(), reveal_duration / 2, scene, animator)

def star_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Draw the star

    This is the star shape that is
    formed by the path that one dot
    on the inner circle follows as
    this inner circle rotates inside
    the outer one.
    """
    reveal = anim.reveal_item(star)
    animator.animate_value([0., 1.], reveal_duration, reveal)
    animation.anim_pointing_arrow(star.item.scene_rect().center(), reveal_duration / 2, scene, animator)

def other_inner_circle_dots_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Draw the other inner-circle dots

    Place the other inner-circle dots
    at the corners of the polygon which
    will follow the inner circle in its
    rotation.
    """
    for which_dot in range(1, dots_count()):
        _anim_other_inner_circle_dots(0, which_dot, animator)

def inner_circle_polygon_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Draw the inner-circle polygon

    This is the polygon that will
    follow the inner circle in its
    rotation.
    """
    _anim_inner_circle_polygon_arrow(0, animation, scene, animator)
    _anim_inner_circle_polygon(0, animator)

def other_circles_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Draw the other inner circles

    These are all the other inner circles,
    their dots and their polygons.
    """
    _anim_inner_circle_polygon_arrow(1, animation, scene, animator)
    for which_inner in range(1, inner_count()):
        _anim_inner_circle(which_inner, animator)
        for which_dots in range(0, dots_count()):
            _anim_other_inner_circle_dots(which_inner, which_dots, animator)
        _anim_inner_circle_polygon(which_inner, animator)
                

def inter_circle_polygons_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Draw the inter-circle polygons

    These are the polygons formed
    by linking the corresponding
    dots on each inner circle.
    They will also rotate when
    the inner circles rotate and
    surprisingly not deform.
    """
    polys = [inter_polygons[which_dot] for which_dot in range(0, dots_count())]
    for poly in polys:
        animator.animate_value([0., 1.], reveal_duration, anim.reveal_item(poly))

def rotate_all_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Animate all polygons

    Rotate the inner circle inside
    the outer one dragging along
    the polygons in a curious dance.
    """
    for which_inner in range(inner_count()):
        anim.roll_points_on_circle_in_circle(animator, 2. * animation_speedup(), inner_circles[which_inner].item, outer_circle.item, skip(), inner_dots_pos[which_inner])

    animation.anim_pointing_arrow(outer_circle.item.get_circumference_point(-math.pi / 4), reveal_duration, scene, animator)


#################################################################
#
# Animation

rotating_stars = anim.simple_animation.from_module(globals())
