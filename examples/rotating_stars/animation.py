import anim

from PyQt5.QtGui import QTransform, QPolygonF
from PyQt5.QtCore import QPointF, QLineF

class animation(anim.animation):
    def __init__(self, scene: anim.scene, sides: int = 7, skip: int = 3, ratio = 0.9) -> None:
        super().__init__("Rotating Stars", "Mathologer 3-4-7 Miracle: rotating interlinked polygons following a star trajectory.")
        self.sides_option = anim.option("Number of branches", "", sides, 2, 20)
        self.skip_option = anim.option("Star branch skip", "", skip, 1, 100)
        self.ratio_option = anim.option("Percent of radius", "", int(ratio * 100), 0, 100)
        self.add_options(self.sides_option)
        self.add_options(self.skip_option)
        self.add_options(self.ratio_option)
        self.circle_rotation_pos = 0
        self.reset(scene)

    @property
    def sides(self):
        return self.sides_option.value

    @property
    def skip(self):
        return min(self.skip_option.value, self.sides - 1)

    @property
    def inner_circle_ratio(self):
        return float(self.skip) / float(self.sides)

    @property
    def inner_count(self):
        return self.sides - self.skip

    @property
    def dots_count(self):
        return self.skip

    @property
    def inner_circle_dot_ratio(self):
        return float(self.ratio_option.value) / 100.

    def reset(self, scene: anim.scene) -> None:
        super().reset(scene)
        self.circle_rotation_pos_steps = 1000 // max(self.skip, 1)
        self.circle_rotation_pos = (self.circle_rotation_pos + 1) % (self.circle_rotation_pos_steps * self.sides)
        self.generate_actors(scene)
        self.generate_shots()

    def generate_actors(self, scene: anim.scene) -> None:
        self._gen_star(scene)
        self._gen_outer_circle(scene)
        self._gen_inner_circles(scene)
        self._gen_dots(scene)
        self._gen_inner_circle_polygons(scene)
        self._gen_inter_circle_polygons(scene)

    def generate_shots(self) -> None:
        self._anim_outer_circle()
        self._anim_inner_circle()
        self._anim_inner_circle_dot()
        self._anim_star()
        self._anim_other_inner_circle_dots()
        self._anim_inner_circle_polygon()
        self._anim_other_inner_circles()
        self._anim_inter_circle_polygons()
        self._anim_all()

    def option_changed(self, scene: anim.scene, animator: anim.animator, option: anim.option) -> None:
        self.reset(scene)
        anim.shot.play_all(self.shots, scene, animator)


    #################################################################
    #
    # Helper functions

    def _get_anti_skip_ratio(self):
        if self.inner_count:
            return 1. / float(self.inner_count)
        return 1.

    def _gen_inner_center(self, which_inner: int):
        """
        Generate the position of the center of an inner circle.
        """
        inner_center = QPointF(1. - self.inner_circle_ratio, 0) * anim.items.outer_size
        angle = 360. * which_inner * self._get_anti_skip_ratio()
        return QTransform().rotate(angle).map(inner_center)

    def _gen_dot_pos(self, which_inner: int, which_dot: int):
        """
        Generate the position of a dot on an inner circle.
        """
        dot_pos = QPointF(self.inner_circle_ratio * self.inner_circle_dot_ratio, 0) * anim.items.outer_size
        dot_angle = 360.0 * which_dot / float(max(self.skip, 1))
        return QTransform().rotate(dot_angle).map(dot_pos)


    #################################################################
    #
    # Actors.

    def _gen_star(self, scene: anim.scene):
        """
        Create the star by rotating the inner circle leaving a trail
        formed by the dot on the inner circle, forming the star.
        Keep it in the animator to avoid re-recreating on each frame.
        """
        # star_segments = 240 // max(self.skip, 1)
        # pts = []
        # for i in range(star_segments * self.skip + 1):
        #     new_pos = self._gen_dot_pos(0, 0, i, star_segments)
        #     pts.append(new_pos)
        pts = []
        for which_dot in range(self.dots_count):
            new_pos = self._gen_dot_pos(0, which_dot)
            pts.append(new_pos)
        poly = anim.items.create_polygon(pts, anim.items.dark_gray_color)
        self.star = anim.actor("star", "The star that the dots on the inner circle follow.", poly)
        self.add_actors(self.star, scene)

    def _gen_outer_circle(self, scene: anim.scene):
        circle = anim.items.create_circle(anim.items.outer_size + anim.items.line_width, anim.items.dark_blue_color, anim.items.line_width * 2)
        circle.setPos(0, 0)
        self.outer_circle = anim.actor("outer circle", "", circle)
        self.add_actors(self.outer_circle, scene)

    def _gen_inner_circles(self, scene: anim.scene):
        self.inner_circles = []
        for which_inner in range(self.inner_count):
            circle = anim.items.create_disk(self.inner_circle_ratio * anim.items.outer_size)
            circle.setPos(self._gen_inner_center(which_inner))
            self.inner_circles.append(anim.actor("inner circle", "", circle))
        self.add_actors(self.inner_circles, scene)

    def _gen_dots(self, scene: anim.scene):
        self.inner_dots = []
        for which_inner in range(0, self.inner_count):
            self.inner_dots.append(list())
            for which_dot in range(0, self.dots_count):
                dot = anim.items.create_disk(anim.items.dot_size, anim.items.orange_color, self.inner_circles[which_inner])
                dot.setPos(self._gen_dot_pos(which_inner, which_dot))
                self.inner_dots[which_inner].append(anim.actor("inner circle dot", "", dot))
        self.add_actors(self.inner_dots)

    def _gen_inner_circle_polygons(self, scene: anim.scene):
        """
        Draw the polygon generated by the inner circle dots.
        """
        self.inner_polygons = []
        for which_inner in range(0, self.inner_count):
            pts = []
            for which_dot in range(0, self.dots_count):
                pts.append(self._gen_dot_pos(which_inner, which_dot))
            poly = anim.items.create_polygon(pts, anim.items.green_color, anim.items.line_width, self.inner_circles[which_inner])
            self.inner_polygons.append(anim.actor("inner polygon", "", poly))
        self.add_actors(self.inner_polygons)

    def _gen_inter_circle_polygons(self, scene: anim.scene):
        """
        Draw the polygon generated by the corresponding dots
        in all inner circles.
        """
        self.inter_polygons = []
        for which_dot in range(0, self.dots_count):
            pts = []
            for which_inner in range(0, self.inner_count):
                pts.append(self._gen_dot_pos(which_inner, which_dot) + self._gen_inner_center(which_inner))
            poly = anim.items.create_polygon(pts, anim.items.blue_color)
            self.inter_polygons.append(anim.actor("outer polygon", "", poly))
        self.add_actors(self.inter_polygons, scene)


    #################################################################
    #
    # Shots

    def _anim_outer_circle(self):
        """
        Draw the outer circle inside which the star will be made.
        """
        def prep_anim(scene: anim.scene, animator: anim.animator):
            pass
            # anim.reveal_with_opacity(animator, self.outer_circle)

        self.add_shots(anim.shot("Draw the outer circle", "", prep_anim))

    def _anim_inner_circle(self, which_inner: int = 0):
        """
        Draw the inner circle with a radius a fraction of the outer circle.
        That fraction is given as the ratio.
        """
        circle = self.inner_circles[which_inner]
        def prep_anim(scene: anim.scene, animator: anim.animator):
            pass
            # anim.reveal_with_opacity(animator, circle)

        self.add_shots(anim.shot("Draw the inner circle", "", prep_anim))

    def _prep_anim_dot(self, scene: anim.scene, animator: anim.animator, which_dot: int, which_inner: int):
        dot = self.inner_dots[which_inner][which_dot]
        # anim.reveal_with_opacity(animator, dot)

    def _anim_inner_circle_dot(self, which_inner: int = 0):
        """
        Draw the dot on the inner circle at the radius ratio given.
        The ratio should be between 0 and 1.
        """
        def prep_anim(scene: anim.scene, animator: anim.animator):
            self._prep_anim_dot(scene, animator, 0, which_inner)

        self.add_shots(anim.shot("Draw the dot on the inner circle", "", prep_anim))

    def _anim_star(self):
        """
        Draw the star by rotating the inner circle leaving a trail
        formed by the dot on the inner circle, forming the star.
        """
        def prep_anim(scene: anim.scene, animator: anim.animator):
            pass
            # anim.reveal_with_opacity(animator, self.star)

        self.add_shots(anim.shot("Draw the star", "", prep_anim))

    def _anim_other_inner_circle_dots(self, which_inner: int = 0):
        """
        Draw the other dots on the inner circle that are added
        when the circle passes over the star's spikes.
        """
        def prep_anim(scene: anim.scene, animator: anim.animator):
            for which_dot in range(1, self.dots_count):
                self._prep_anim_dot(scene, animator, which_dot, which_inner)

        self.add_shots(anim.shot("Draw the other dots on the inner circle", "", prep_anim))

    def _anim_inner_circle_polygon(self, which_inner: int = 0):
        """
        Draw the polygon generated by the inner circle dots.
        """
        def prep_anim(scene: anim.scene, animator: anim.animator):
            poly = self.inner_polygons[which_inner]
            pass
            # anim.reveal_with_opacity(animator, poly)

        self.add_shots(anim.shot("Draw the inner circle polygon", "", prep_anim))

    def _anim_other_inner_circles(self):
        """
        Draw the additional inner circles and their dots and polygon.
        """
        for which_inner in range(1, self.inner_count):
            self._anim_inner_circle(which_inner)
            self._anim_inner_circle_dot(which_inner)
            self._anim_other_inner_circle_dots(which_inner)
            self._anim_inner_circle_polygon(which_inner)

    def _anim_inter_circle_polygons(self):
        """
        Draw the polygon _animd by the corresponding dots
        in all inner circles.
        """
        def prep_anim(scene: anim.scene, animator: anim.animator):
            for which_dot in range(0, self.dots_count):
                poly = self.inter_polygons[which_dot]
                # anim.reveal_with_opacity(animator, poly)

        self.add_shots(anim.shot("Draw the inter-circle polygons", "", prep_anim))

    def _anim_all(self):
        """
        Animate all the inner circles and their polygons.
        """
        def prep_anim(scene: anim.scene, animator: anim.animator):
            for which_inner in range(self.inner_count):
                circle = self.inner_circles[which_inner]
                outer_angle = 360. * self.sides
                inner_angle = outer_angle / self.inner_circle_ratio
                anim.rotate(animator, circle, inner_angle, 0.)
                anim.rotate_around(animator, circle, 0., outer_angle, 0., 0.)

        self.add_shots(anim.shot("Animate all", "", prep_anim))
