import anim

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
    return sides() - skip()

def dots_count():
    return skip()

def inner_circle_dot_ratio():
    return float(ratio_option.value) / 100.

def anti_count_ratio():
    if inner_count() > 0:
        return 1. / float(inner_count())
    return 1.

def animation_speedup():
    return inner_count()

reveal_duration = 0.3


#################################################################
#
# Actors

inner_centers = []
inner_dots_pos = []

outer_circle = None
inner_circles = []
inner_dots = []
inner_polygons = []
inter_polygons = []
star = None

def generate_actors(animation: anim.animation, scene: anim.scene):
    global inner_centers, inner_dots_pos
    global outer_circle, inner_circles, inner_dots, inner_polygons, inter_polygons, star

    inner_centers = []
    inner_dots_pos = []

    outer_circle = None
    inner_circles = []
    inner_dots = []
    inner_polygons = []
    inter_polygons = []
    star = None

    inner_center = anim.point((1. - inner_circle_ratio()) * anim.items.outer_size, 0)
    dot_pos = anim.point(inner_circle_ratio() * inner_circle_dot_ratio() * anim.items.outer_size, 0)

    for which_inner in range(inner_count()):
        angle = 360. * which_inner * anti_count_ratio()
        inner_centers.append(anim.point(anim.trf.rotate_around_origin(inner_center, angle)))
        inner_dots_pos.append(list())
        for which_dot in range(dots_count()):
            dot_angle = 360.0 * which_dot / float(max(skip(), 1))
            inner_dots_pos[which_inner].append(anim.relative_point(inner_centers[which_inner], anim.trf.rotate_around_origin(dot_pos, dot_angle)))

    outer_angle = 360. * skip()
    inner_angle = 360. * inner_count()
    center = anim.point(inner_centers[0].original_point)
    dot = anim.relative_point(center, inner_dots_pos[0][0].original_point)
    pts = []
    star_segment_count = 240
    for i in range(star_segment_count):
        angle = outer_angle * float(i) / float(star_segment_count)
        center.set_point(anim.trf.rotate_around_origin(center.original_point, angle))
        angle = -inner_angle * float(i) / float(star_segment_count)
        dot.set_point(anim.trf.rotate_around_origin(dot.original_point, angle))
        pts.append(anim.point(dot))

    star = anim.actor("star", "The star that the dots on the inner circle follow.",
        anim.items.create_polygon(pts, anim.items.dark_gray_color))

    outer_circle = anim.actor("outer circle", "",
        anim.items.create_circle(anim.point(0., 0.), anim.items.outer_size + anim.items.line_width, anim.items.dark_blue_color, anim.items.line_width * 2))

    inner_circles = []
    inner_radius = inner_circle_ratio() * anim.items.outer_size
    for center in inner_centers:
        circle = anim.items.create_disk(center, inner_radius)
        inner_circles.append(anim.actor("inner circle", "", circle))

    inner_dots = []
    for which_inner in range(0, inner_count()):
        inner_dots.append(list())
        for which_dot in range(0, dots_count()):
            center = inner_dots_pos[which_inner][which_dot]
            dot = anim.items.create_disk(center, anim.items.dot_size, anim.items.orange_color)
            inner_dots[which_inner].append(anim.actor("inner circle dot", "", dot))

    inner_polygons = []
    for which_inner in range(0, inner_count()):
        poly = anim.items.create_polygon(inner_dots_pos[which_inner], anim.items.green_color, anim.items.line_width)
        inner_polygons.append(anim.actor("inner polygon", "", poly))

    inter_polygons = []
    for which_dot in range(0, dots_count()):
        pts = [inner_dots_pos[which_inner][which_dot] for which_inner in range(0, inner_count())]
        poly = anim.items.create_polygon(pts, anim.items.blue_color)
        inter_polygons.append(anim.actor("outer polygon", "", poly))

    animation.add_actors([outer_circle, inner_circles, inner_dots, inner_polygons, inter_polygons, star], scene)


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
        outer_angle = 360. * skip()
        inner_angle = 360. * inner_count()
        for which_inner in range(inner_count()):
            center = inner_centers[which_inner]
            rot_center = anim.rotate_point_around(center, anim.point(0., 0.))
            animator.animate_value(0., outer_angle, 2. * animation_speedup(), rot_center)
            for which_dot in range(dots_count()):
                dot = inner_dots_pos[which_inner][which_dot]
                rot_dot = anim.rotate_point_around(dot, anim.point(0., 0.))
                animator.animate_value(0., -inner_angle, 2. * animation_speedup(), rot_dot)

        outer_circle_rect = outer_circle.item.scene_rect()
        outer_circle_radius = outer_circle_rect.width() / 2.75
        outer_circle_corner = outer_circle_rect.center() + anim.static_point(outer_circle_radius, -outer_circle_radius)
        animation.anim_pointing_arrow(outer_circle_corner, reveal_duration, scene, animator)

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
