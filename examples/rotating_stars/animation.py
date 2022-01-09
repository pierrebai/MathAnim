import anim

from PyQt5.QtGui import QTransform, QPolygonF
from PyQt5.QtCore import QPointF, QLineF

class animation():
    """
    animator using a Qt graphics scene to show step-by-step changes.
    """

    def __init__(self, star, options, *args, **kwargs):
        self.star = star
        self.options = options
        self.reset()


    #################################################################
    #
    # Helper functions

    def _get_outer_angle(self, rot_pos: int, rot_steps: int):
        if rot_steps:
            return 360. * float(rot_pos) / float(rot_steps)
        return 0.

    def _get_anti_skip_ratio(self):
        if self.star.sides != self.star.skip:
            return 1. / float(self.star.sides - self.star.skip)
        return 1.

    def _get_inner_center(self, which_inner: int, rot_pos: int, rot_steps: int):
        """
        Calculate the center position of an inner circle.
        """
        inner_center = QPointF(1. - self.star.inner_circle_ratio, 0)
        if self.star.sides != self.star.skip:
            outer_angle = self._get_outer_angle(rot_pos, rot_steps)
            angle = 360. * which_inner * self._get_anti_skip_ratio()
            inner_center = QTransform().rotate(angle + outer_angle).map(inner_center)
        return inner_center

    def _gen_all_dots_for_rot(self, rot_pos: int, rot_steps: int):
        """
        Generate all positions for all dots on all inner circle.
        Fills a 2D array called inner_dots_pos indexed by inner circle
        and dots.
        """
        outer_angle = self._get_outer_angle(rot_pos, rot_steps)
        ratio = float(self.star.skip) * self._get_anti_skip_ratio()
        inner_angle = -outer_angle / ratio
        dots_pos = []
        inner_count = self.star.sides - self.star.skip
        for which_inner in range(0, inner_count):
            dots_pos.append(list())
            inner_center = self._get_inner_center(which_inner, rot_pos, rot_steps)
            for which_dot in range(0, self.star.skip):
                dot_pos = QPointF(self.star.inner_circle_ratio * self.star.inner_circle_dot_ratio, 0)
                dot_angle = 360.0 * which_dot / float(max(self.star.skip, 1))
                dot_pos = QTransform().rotate(dot_angle + inner_angle).map(dot_pos)
                dot_pos += inner_center
                dot_pos *= anim.items.outer_size
                dots_pos[which_inner].append(dot_pos)
        return dots_pos

    def _gen_all_dots_pos(self):
        """
        Generate all positions for all dots on all inner circle.
        Fills a 2D array called inner_dots_pos indexed by inner circle
        and dots.
        """
        self.inner_dots_pos = self._gen_all_dots_for_rot(self.circle_rotation_pos, self.circle_rotation_pos_steps)

    def _gen_dot(self, scene: anim.scene, which_dot: int, which_inner: int):
        dot_pos = self.inner_dots_pos[which_inner][which_dot]
        dot = anim.items.create_disk(anim.items.dot_size, anim.items.orange_color)
        dot.setPos(dot_pos)
        scene.add_item(dot)

    def _gen_star_points(self):
        """
        Create the star by rotating the inner circle leaving a trail
        formed by the dot on the inner circle, forming the star.
        Keep it in the animator to avoid re-recreating on each frame.
        """
        star_segments = 240 // max(self.star.skip, 1)
        all_pos = []
        for i in range(star_segments * self.star.skip + 1):
            new_pos = self._gen_all_dots_for_rot(i, star_segments)
            if len(new_pos) and len(new_pos[0]):
                new_point = new_pos[0][0]
                all_pos.append(new_point)
        if len(all_pos):
            self.star_points = all_pos
        else:
            self.star_points = None


    #################################################################
    #
    # Animator base class function overrides

    def reset(self):
        self.circle_rotation_pos = 0.
        self.circle_rotation_pos_steps = 1000 // max(self.star.skip, 1)
        self._gen_all_dots_pos()
        self._gen_star_points()
        
    def generate_outer_circle(self):
        """
        Draw the outer circle inside which the star will be made.
        """
        def prep_anim(scene: anim.scene, animator: anim.animator):
            color = anim.items.dark_blue_color if self.options.draw_outer_circle else anim.items.no_color
            circle = anim.items.create_circle(anim.items.outer_size + anim.items.line_width, color, anim.items.line_width * 2)
            circle.setPos(0, 0)
            scene.add_item(circle)

        return anim.shot("Draw the outer circle", prep_anim)

    def generate_inner_circle(self, which_inner: int = 0):
        """
        Draw the inner circle with a radius a fraction of the outer circle.
        That fraction is given as the ratio.
        """
        if not self.options.draw_inner_circles:
            return None

        def prep_anim(scene: anim.scene, animator: anim.animator):
            inner_center = self._get_inner_center(which_inner, self.circle_rotation_pos, self.circle_rotation_pos_steps)
            circle = anim.items.create_disk(self.star.inner_circle_ratio * anim.items.outer_size)
            circle.setPos(inner_center * anim.items.outer_size)
            scene.add_item(circle)

        return anim.shot("Draw the inner circle", prep_anim)

    def generate_inner_circle_dot(self, which_inner: int = 0):
        """
        Draw the dot on the inner circle at the radius ratio given.
        The ratio should be between 0 and 1.
        """
        if not self.options.draw_dots:
            return None

        def prep_anim(scene: anim.scene, animator: anim.animator):
            self._gen_dot(scene, 0, which_inner)

        return anim.shot("Draw the dot on the inner circle", prep_anim)

    def generate_star(self):
        """
        Draw the star by rotating the inner circle leaving a trail
        formed by the dot on the inner circle, forming the star.
        """
        if not self.options.draw_star:
            return None

        if not self.star_points:
            return None

        def prep_anim(scene: anim.scene, animator: anim.animator):
            poly = anim.items.create_polygon(self.star_points, anim.items.dark_gray_color)
            scene.add_item(poly)

        return anim.shot("Draw the star", prep_anim)

    def generate_other_inner_circle_dots(self, which_inner: int = 0):
        """
        Draw the other dots on the inner circle that are added
        when the circle passes over the star's spikes.
        """
        if not self.options.draw_dots:
            return None

        def prep_anim(scene: anim.scene, animator: anim.animator):
            for which_dot in range(1, self.star.skip):
                self._gen_dot(scene, which_dot, which_inner)

        return anim.shot("Draw the other dots on the inner circle", prep_anim)

    def generate_inner_circle_polygon(self, which_inner: int = 0):
        """
        Draw the polygon generated by the inner circle dots.
        """
        if not self.options.draw_intra_circle_polygons:
            return None

        def prep_anim(scene: anim.scene, animator: anim.animator):
            for which_dot in range(0, self.star.skip):
                p1 = self.inner_dots_pos[which_inner][which_dot]
                p2 = self.inner_dots_pos[which_inner][(which_dot + 1) % self.star.skip]
                line = anim.items.create_line(QLineF(p1, p2))
                scene.add_item(line)

        return anim.shot("Draw the inner circle polygon", prep_anim)

    def generate_other_inner_circles(self, starting_from: int = 1):
        """
        Draw the additional inner circles and their dots and polygon.
        """
        shots = []
        def append_valid(shot):
            if not shot:
                return
            shots.append(shot)

        count = self.star.sides - self.star.skip
        for which_inner in range(starting_from, count):
            append_valid(self.generate_inner_circle(which_inner))
            append_valid(self.generate_inner_circle_dot(which_inner))
            append_valid(self.generate_other_inner_circle_dots(which_inner))
            append_valid(self.generate_inner_circle_polygon(which_inner))

        return shots

    def generate_inter_circle_polygons(self):
        """
        Draw the polygon generated by the corresponding dots
        in all inner circles.
        """
        if not self.options.draw_inter_circle_polygons:
            return None

        def prep_anim(scene: anim.scene, animator: anim.animator):
            count = self.star.sides - self.star.skip
            for which_dot in range(0, self.star.skip):
                for which_inner in range(0, count):
                    p1 = self.inner_dots_pos[which_inner][which_dot]
                    p2 = self.inner_dots_pos[(which_inner + 1) % count][which_dot]
                    line = anim.items.create_line(QLineF(p1, p2), anim.items.blue_color)
                    scene.add_item(line)

        return anim.shot("Draw the inter-circle polygons", prep_anim)

    def animate_all(self):
        """
        Animate all the inner circles and their polygons.
        """
        self.circle_rotation_pos = (self.circle_rotation_pos + 1) % (self.circle_rotation_pos_steps * self.star.sides)

        return [
            self._gen_all_dots_pos(),
            self.generate_outer_circle(),
            self.generate_other_inner_circles(0),
            self.generate_star(),
            self.generate_inter_circle_polygons(),
        ]
