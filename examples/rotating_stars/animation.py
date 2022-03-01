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
# Shots

def generate_shots(animation: anim.animation):
    def anim_outer_circle(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
        for actor in animation.actors:
            actor.item.set_opacity(0)
        circle = outer_circle
        animator.animate_value(0., 1., reveal_duration, anim.reveal_item(circle))
        animator.animate_value(0., 1., reveal_duration, anim.reveal_item(scene.pointing_arrow))
        animation.anim_pointing_arrow(circle.item.scene_rect().center(), reveal_duration / 2, scene, animator)

    animation.add_shots(anim.shot(
        "Draw the outer circle",
        "This is the ounter circle\n"
        "insides which the smaller ones\n"
        "will rotate.",
        anim_outer_circle))

    def anim_inner_circle(which_inner: int):
        def prep_anim(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
            circle = inner_circles[which_inner]
            reveal = anim.reveal_item(circle)
            animator.animate_value(0., 1., reveal_duration, reveal)
        return prep_anim

    def anim_inner_circle_arrow(which_inner: int):
        def prep_anim(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
            circle = inner_circles[which_inner]
            animation.anim_pointing_arrow(circle.item.scene_rect().center(), reveal_duration / 2, scene, animator)
            pass
        return prep_anim

    animation.add_shots(anim.shot(
            "Draw an inner circle",
            "This is one of the inner circle that\n"
            "rotates inside the outer circle.",
            [anim_inner_circle(0), anim_inner_circle_arrow(0)]))

    def anim_inner_circle_dot(which_inner: int):
        def prep_anim(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
            dot = inner_dots[which_inner][0]
            reveal = anim.reveal_item(dot)
            animator.animate_value(0., 1., reveal_duration, reveal)
            animation.anim_pointing_arrow(dot.item.scene_rect().center(), reveal_duration / 2, scene, animator)
        return prep_anim

    animation.add_shots(anim.shot(
        "Draw an inner-circle dot",
        "This dot on a circle is one\n"
        "of the corners of a polygon\n"
        "that will rotate, following\n"
        "the circle is it placed on.",
        anim_inner_circle_dot(0)))

    def anim_star(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
        reveal = anim.reveal_item(star)
        animator.animate_value(0., 1., reveal_duration, reveal)
        animation.anim_pointing_arrow(star.item.scene_rect().center(), reveal_duration / 2, scene, animator)

    animation.add_shots(anim.shot(
        "Draw the star",
        "This is the star shape that is\n"
        "formed by the path that one dot\n"
        "on the inner circle follows as\n"
        "this inner circle rotates inside\n"
        "the outer one.",
        anim_star))

    def anim_other_inner_circle_dots(which_inner: int, which_dot: int):
        def prep_anim(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
            dot = inner_dots[which_inner][which_dot]
            reveal = anim.reveal_item(dot)
            animator.animate_value(0., 1., reveal_duration, reveal)
        return prep_anim

    animation.add_shots(anim.shot(
        "Draw the other inner-circle dots",
        "Place the other inner-circle dots\n"
        "at the corners of the polygon which\n"
        "will follow the inner circle in its\n"
        "rotation.",
        [ anim_other_inner_circle_dots(0, which_dot) for which_dot in range(1, dots_count()) ]))

    def anim_inner_circle_polygon(which_inner: int):
        def prep_anim(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
            poly = inner_polygons[which_inner]
            reveal = anim.reveal_item(poly)
            animator.animate_value(0., 1., reveal_duration, reveal)
        return prep_anim

    def anim_inner_circle_polygon_arrow(which_inner: int):
        def prep_anim(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
            poly = inner_polygons[which_inner]
            animation.anim_pointing_arrow(poly.item.scene_rect().center(), reveal_duration / 2, scene, animator)
            pass
        return prep_anim

    animation.add_shots(anim.shot(
        "Draw the inner-circle polygon",
        "This is the polygon that will\n"
        "follow the inner circle in its\n"
        "rotation.",
        [
            anim_inner_circle_polygon_arrow(0),
            anim_inner_circle_polygon(0),
        ]))

    animation.add_shots(anim.shot(
        "Draw the other inner circles",
        "These are all the other inner circles,\n"
        "their dots and their polygons.",
        [
            anim_inner_circle_polygon_arrow(1),
            [
                [ anim_inner_circle(which_inner),
                [ anim_other_inner_circle_dots(which_inner, which_dots) for which_dots in range(0, dots_count())],
                anim_inner_circle_polygon(which_inner) ]
                for which_inner in range(1, inner_count())
            ]
        ]))

    def anim_inter_circle_polygons(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
        polys = [inter_polygons[which_dot] for which_dot in range(0, dots_count())]
        for poly in polys:
            reveal = anim.reveal_item(poly)
            animator.animate_value(0., 1., reveal_duration, reveal)

    animation.add_shots(anim.shot(
        "Draw the inter-circle polygons",
        "These are the polygons formed\n"
        "by linking the corresponding\n"
        "dots on each inner circle.\n"
        "They will also rotate when\n"
        "the inner circles rotate and\n"
        "surprisingly not deform.",
        anim_inter_circle_polygons))

    def anim_all(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
        for which_inner in range(inner_count()):
            anim.roll_points_on_circle_in_circle(animator, 2. * animation_speedup(), inner_circles[which_inner].item, outer_circle.item, skip(), inner_dots_pos[which_inner])

        animation.anim_pointing_arrow(outer_circle.item.get_circumference_point(-math.pi / 4), reveal_duration, scene, animator)

    animation.add_shots(anim.shot(
        "Animate all",
        "Rotate the inner circle inside\n"
        "the outer one dragging along\n"
        "the polygons in a curious dance.",
        anim_all, None, True))


#################################################################
#
# Animation

animation = anim.simple_animation.from_module(globals())
