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
reset_on_change = True

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

reveal_duration = 2.


#################################################################
#
# Points

class points:
    def __init__(self):
        super().__init__()
        self.outer_center   = anim.point(0., 0.)
        self.outer_radius   = anim.outer_size
        self.inner_radius   = self.outer_radius * inner_circle_ratio()
        self.inner_centers  = anim.create_relative_points_around_center(self.outer_center, self.outer_radius - self.inner_radius, inner_count())
        self.dot_radius     = self.inner_radius * inner_circle_dot_ratio()
        self.inner_dots_pos = [anim.create_relative_points_around_center(center, self.dot_radius, skip()) for center in self.inner_centers]

pts: points = None


#################################################################
#
# Geometries

class geometries(anim.geometries):
    def __init__(self, pts):
        super().__init__()
        self._gen_star(pts)
        self._gen_outer_circle(pts)
        self._gen_inner_circles(pts)
        self._gen_inner_dots(pts)
        self._gen_inner_polygons(pts)
        self._gen_inter_polygons(pts)
        self._set_z_orders()

    def _gen_star(self, pts):
        pts = anim.create_roll_circle_in_circle_points(pts.inner_radius, pts.outer_radius, skip(), 240, inner_circle_dot_ratio())
        self.star = anim.create_polygon(pts).outline(anim.dark_gray).thickness(5.)

    def _gen_outer_circle(self, pts):
        self.outer_circle = anim.create_circle(pts.outer_center, anim.outer_size).outline(anim.dark_blue).thickness(anim.line_width * 2)

    def _gen_inner_circles(self, pts):
        self.inner_circles = [anim.create_disk(center, pts.inner_radius) for center in pts.inner_centers]

    def _gen_inner_dots(self, pts):
        self.inner_dots = [
            [anim.create_disk(dot, anim.dot_size).fill(anim.orange) for dot in dots]
                for dots in pts.inner_dots_pos]

    def _gen_inner_polygons(self, pts):
        self.inner_polygons = [anim.create_polygon(dots).outline(anim.green) for dots in pts.inner_dots_pos]

    def _gen_inter_polygons(self, pts):
        outer_dots_pos = anim.transpose_lists(pts.inner_dots_pos)
        self.inter_polygons = [anim.create_polygon(dots).outline(anim.blue) for dots in outer_dots_pos]

    def _set_z_orders(self):
        for c in self.inner_circles:
            c.set_z_order(-1)

        for ds in self.inner_dots:
            for d in ds:
                d.set_z_order(1)

geo: geometries = None


#################################################################
#
# Actors

def generate_actors(animation: anim.animation, scene: anim.scene):
    global pts; pts = points()
    global geo; geo = geometries(pts)

    animation.add_actor(anim.actor("star", "The star that the dots on the inner circle follow.", geo.star), scene)
    animation.add_actor(anim.actor("outer circle", "", geo.outer_circle), scene)
    animation.add_actors([anim.actor("inner circle", "", circle) for circle in geo.inner_circles], scene)
    animation.add_actors([
        [anim.actor("inner circle dot", "", dot) for dot in dots]
            for dots in geo.inner_dots], scene)
    animation.add_actors([anim.actor("inner polygon", "", poly) for poly in geo.inner_polygons], scene)
    animation.add_actors([anim.actor("outer polygon", "", poly) for poly in geo.inter_polygons], scene)

    rect_radius =  pts.outer_radius * 1.2
    scene.add_item(anim.create_invisible_rect(-rect_radius, -rect_radius, rect_radius * 2, rect_radius * 2))


#################################################################
#
# Prepare animation

def prepare_playing(animation: anim.animation, scene: anim.scene, animator: anim.animator):
    geo.reset()


#################################################################
#
# Reused animations

def _anim_inner_circle(which_inner: int, animator: anim.animator):
    anim.anim_reveal_radius(animator, reveal_duration, geo.inner_circles[which_inner], 1.3)

def _anim_inner_circle_dots(which_inner: int, which_dot: int, animator: anim.animator):
    anim.anim_reveal_radius(animator, reveal_duration, geo.inner_dots[which_inner][which_dot], 4)

def _anim_inner_circle_polygon(which_inner: int, animator: anim.animator):
    anim.anim_reveal_thickness(animator, reveal_duration, geo.inner_polygons[which_inner])

def _anim_inner_circle_polygon_arrow(which_inner: int, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    if which_inner < len(geo.inner_polygons):
        poly = geo.inner_polygons[which_inner]
        mid_line = (poly.points[0] + poly.points[-1]) / 2.
        animation.anim_pointing_arrow(mid_line, reveal_duration / 2, scene, animator)


#################################################################
#
# Shots

def outer_circle_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Draw the outer circle

    This is the outer circle,
    in which the smaller one
    will rotate.
    """
    circle = geo.outer_circle
    animator.animate_value([0., 1.], reveal_duration, anim.reveal_item(circle))
    animator.animate_value([0., 1.], reveal_duration, anim.reveal_item(scene.pointing_arrow))
    point_on_circle = anim.create_relative_point_around_center(circle.center, circle.radius, -anim.qpi)
    animation.anim_pointing_arrow(point_on_circle, reveal_duration / 2, scene, animator)

def inner_circle_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Draw an inner circle

    This is one of the inner
    circle that rotates inside
    the outer circle.
    """
    _anim_inner_circle(0, animator)
    circle = geo.inner_circles[0]
    animation.anim_pointing_arrow(circle.scene_rect().center(), reveal_duration / 2, scene, animator)

def inner_circle_dot_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Draw an inner-circle dot

    This dot on a circle is
    one of the corners of a
    polygon. This polygon
    will spin, dragged along
    by the circle beneath it.
    """
    _anim_inner_circle_dots(0, 0, animator)
    animation.anim_pointing_arrow(geo.inner_dots[0][0].scene_rect().center(), reveal_duration / 2, scene, animator)

def star_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Draw the star

    This is the star that is
    traced by one of the dots
    on the inner circle as it
    rotates inside the outer
    circle.
    """
    anim.anim_reveal_thickness(animator, reveal_duration, geo.star)
    animation.anim_pointing_arrow(geo.star.scene_rect().center(), reveal_duration / 2, scene, animator)

def other_inner_circle_dots_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Draw the other inner-circle dots

    The other inner-circle
    dots are placed to form
    the corners of the polygon
    attached on top the inner
    circle.
    """
    if dots_count() < 2:
        return
    for which_dot in range(1, dots_count()):
        _anim_inner_circle_dots(0, which_dot, animator)
    animation.anim_pointing_arrow(geo.inner_dots[0][1].scene_rect().center(), reveal_duration / 2, scene, animator)

def inner_circle_polygon_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Draw the inner-circle polygon

    This is the polygon which
    follows the inner circle
    in its rotation.
    """
    _anim_inner_circle_polygon_arrow(0, animation, scene, animator)
    _anim_inner_circle_polygon(0, animator)

def other_circles_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Draw the other inner circles

    These are all the other
    inner circles, their dots
    and their polygons.
    """
    _anim_inner_circle_polygon_arrow(1, animation, scene, animator)
    for which_inner in range(1, inner_count()):
        _anim_inner_circle(which_inner, animator)
        for which_dots in range(0, dots_count()):
            _anim_inner_circle_dots(which_inner, which_dots, animator)
        _anim_inner_circle_polygon(which_inner, animator)
                

def inter_circle_polygons_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Draw the inter-circle polygons

    By linking each group of
    corresponding dots on each
    inner circle, we form these
    inter-circle polygons.

    These polygons will also
    rotate when dragged along
    by the inner circles and,
    surprisingly, will keep
    their rigid shape.
    """
    polys = [geo.inter_polygons[which_dot] for which_dot in range(0, dots_count())]
    for poly in polys:
        animator.animate_value([0., 1.], reveal_duration, anim.reveal_item(poly))

def rotate_all_shot(shot: anim.shot, animation: anim.animation, scene: anim.scene, animator: anim.animator):
    """
    Animate all polygons

    Rotate the inner circles
    inside the outer ones,
    dragging along the polygons
    in a curious dance.
    """
    shot.repeat = True

    for which_inner in range(inner_count()):
        anim.roll_points_on_circle_in_circle(animator, 2. * animation_speedup(),
            geo.inner_circles[which_inner],
            geo.outer_circle, skip(),
            pts.inner_dots_pos[which_inner])

    animation.anim_pointing_arrow(geo.outer_circle.get_circumference_point(-math.pi / 4), reveal_duration, scene, animator)


#################################################################
#
# Animation

rotating_stars = anim.simple_animation.from_module(globals())
