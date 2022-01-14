import anim

from anim.ui import get_shown_actors_by_names, apply_shown_to_actors

class animation(anim.animation):
    def __init__(self, scene: anim.scene, sides: int = 7, skip: int = 3, ratio = 0.9) -> None:
        super().__init__("Rotating Stars", "Mathologer 3-4-7 Miracle: rotating interlinked polygons following a star trajectory.")
        self.sides_option = anim.option("Number of branches", "Number of branches on the star that the dots follows.", sides, 2, 20)
        self.skip_option = anim.option("Star branch skip", "How many branches are skipped to go from one branch to the next.", skip, 1, 100)
        self.ratio_option = anim.option("Percent of radius", "The position of the dots as a percentage of the radius of the circle they are on.", int(ratio * 100), 0, 100)
        self.add_options(self.sides_option)
        self.add_options(self.skip_option)
        self.add_options(self.ratio_option)
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

    @property
    def anti_count_ratio(self):
        if self.inner_count > 0:
            return 1. / float(self.inner_count)
        return 1.

    @property
    def animation_speedup(self):
        return self.inner_count

    @property
    def reveal_duration(self):
        return 0.3

    def reset(self, scene: anim.scene) -> None:
        was_last = (self.current_shot == len(self.shots) - 1)
        shown_by_names = get_shown_actors_by_names(self)

        super().reset(scene)

        self.generate_actors(scene)
        apply_shown_to_actors(self, shown_by_names)
        self.generate_shots()

        if was_last:
            self.current_shot = len(self.shots) - 1
        else:
            self.current_shot = 0

    def generate_actors(self, scene: anim.scene) -> None:
        self._gen_points()
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
        # The reset function regenerate the actors, anims and shots,
        # which will make the animator pick up the new animations on the fly.
        self.reset(scene)
        # Stopping the animator only triggers its anim_done_callback,
        # which in the main triggers the next shot to be played.
        animator.stop()


    #################################################################
    #
    # Actors.

    def _gen_points(self):
        inner_centers = []
        inner_dots_pos = []

        inner_center = anim.point((1. - self.inner_circle_ratio) * anim.items.outer_size, 0)
        dot_pos = anim.point(self.inner_circle_ratio * self.inner_circle_dot_ratio * anim.items.outer_size, 0)

        for which_inner in range(self.inner_count):
            angle = 360. * which_inner * self.anti_count_ratio
            inner_centers.append(anim.point(anim.trf.rotate_around_origin(inner_center, angle)))
            inner_dots_pos.append(list())
            for which_dot in range(self.dots_count):
                dot_angle = 360.0 * which_dot / float(max(self.skip, 1))
                inner_dots_pos[which_inner].append(anim.relative_point(inner_centers[which_inner], anim.trf.rotate_around_origin(dot_pos, dot_angle)))

        self.inner_centers = inner_centers
        self.inner_dots_pos = inner_dots_pos

    def _gen_star(self, scene: anim.scene):
        """
        Create the star by rotating the inner circle leaving a trail
        formed by the dot on the inner circle, forming the star.
        Keep it in the animator to avoid re-recreating on each frame.
        """
        outer_angle = 360. * self.skip
        inner_angle = 360. * self.inner_count
        center = anim.point(self.inner_centers[0].original_point)
        dot = anim.relative_point(center, self.inner_dots_pos[0][0].original_point)
        pts = []
        star_segment_count = 240
        for i in range(star_segment_count):
            angle = outer_angle * float(i) / float(star_segment_count)
            center.set_point(anim.trf.rotate_around_origin(center.original_point, angle))
            angle = -inner_angle * float(i) / float(star_segment_count)
            dot.set_point(anim.trf.rotate_around_origin(dot.original_point, angle))
            pts.append(anim.point(dot))
        poly = anim.items.create_polygon(pts, anim.items.dark_gray_color)
        self.star = anim.actor("star", "The star that the dots on the inner circle follow.", poly)
        self.add_actors(self.star, scene)

    def _gen_outer_circle(self, scene: anim.scene):
        radius = anim.items.outer_size + anim.items.line_width
        circle = anim.items.create_circle(anim.point(0., 0.), radius, anim.items.dark_blue_color, anim.items.line_width * 2)
        self.outer_circle = anim.actor("outer circle", "", circle)
        self.add_actors(self.outer_circle, scene)

    def _gen_inner_circles(self, scene: anim.scene):
        self.inner_circles = []
        inner_radius = self.inner_circle_ratio * anim.items.outer_size
        for center in self.inner_centers:
            circle = anim.items.create_disk(center, inner_radius)
            self.inner_circles.append(anim.actor("inner circle", "", circle))
        self.add_actors(self.inner_circles, scene)

    def _gen_dots(self, scene: anim.scene):
        self.inner_dots = []
        for which_inner in range(0, self.inner_count):
            self.inner_dots.append(list())
            for which_dot in range(0, self.dots_count):
                center = self.inner_dots_pos[which_inner][which_dot]
                dot = anim.items.create_disk(center, anim.items.dot_size, anim.items.orange_color)
                self.inner_dots[which_inner].append(anim.actor("inner circle dot", "", dot))
        self.add_actors(self.inner_dots, scene)

    def _gen_inner_circle_polygons(self, scene: anim.scene):
        """
        Draw the polygon generated by the inner circle dots.
        """
        self.inner_polygons = []
        for which_inner in range(0, self.inner_count):
            poly = anim.items.create_polygon(self.inner_dots_pos[which_inner], anim.items.green_color, anim.items.line_width)
            self.inner_polygons.append(anim.actor("inner polygon", "", poly))
        self.add_actors(self.inner_polygons, scene)

    def _gen_inter_circle_polygons(self, scene: anim.scene):
        """
        Draw the polygon generated by the corresponding dots
        in all inner circles.
        """
        self.inter_polygons = []
        for which_dot in range(0, self.dots_count):
            pts = [self.inner_dots_pos[which_inner][which_dot] for which_inner in range(0, self.inner_count)]
            poly = anim.items.create_polygon(pts, anim.items.blue_color)
            self.inter_polygons.append(anim.actor("outer polygon", "", poly))
        self.add_actors(self.inter_polygons, scene)

    def _hide_all_actors(self):
        """
        Hide all actors.
        """
        for actor in self.actors:
            actor.item.setOpacity(0)


    #################################################################
    #
    # Shots

    def _anim_outer_circle(self):
        """
        Draw the outer circle inside which the star will be made.
        """
        def prep_anim(scene: anim.scene, animator: anim.animator):
            self._hide_all_actors()
            circle = self.outer_circle
            reveal = anim.reveal_item(circle)
            animator.animate_value(0., 1., self.reveal_duration, reveal)

        self.add_shots(anim.shot("Draw the outer circle", "", prep_anim))

    def _anim_inner_circle(self, which_inner: int = 0):
        """
        Draw the inner circle with a radius a fraction of the outer circle.
        That fraction is given as the ratio.
        """
        def prep_anim(scene: anim.scene, animator: anim.animator):
            circle = self.inner_circles[which_inner]
            reveal = anim.reveal_item(circle)
            animator.animate_value(0., 1., self.reveal_duration, reveal)

        self.add_shots(anim.shot("Draw the inner circle", "", prep_anim))

    def _anim_inner_circle_dot(self, which_inner: int = 0):
        """
        Draw the dot on the inner circle at the radius ratio given.
        The ratio should be between 0 and 1.
        """
        def prep_anim(scene: anim.scene, animator: anim.animator):
            dot = self.inner_dots[which_inner][0]
            reveal = anim.reveal_item(dot)
            animator.animate_value(0., 1., self.reveal_duration, reveal)

        self.add_shots(anim.shot("Draw the dot on the inner circle", "", prep_anim))

    def _anim_star(self):
        """
        Draw the star by rotating the inner circle leaving a trail
        formed by the dot on the inner circle, forming the star.
        """
        def prep_anim(scene: anim.scene, animator: anim.animator):
            star = self.star
            reveal = anim.reveal_item(star)
            animator.animate_value(0., 1., self.reveal_duration, reveal)

        self.add_shots(anim.shot("Draw the star", "", prep_anim))

    def _anim_other_inner_circle_dots(self, which_inner: int = 0):
        """
        Draw the other dots on the inner circle that are added
        when the circle passes over the star's spikes.
        """
        def prep_anim(scene: anim.scene, animator: anim.animator):
            dots = [self.inner_dots[which_inner][which_dot] for which_dot in range(1, self.dots_count)]
            if dots:
                for dot in dots:
                    reveal = anim.reveal_item(dot)
                    animator.animate_value(0., 1., self.reveal_duration, reveal)
            else:
                animator.check_all_anims_done()

        self.add_shots(anim.shot("Draw the other dots on the inner circle", "", prep_anim))

    def _anim_inner_circle_polygon(self, which_inner: int = 0):
        """
        Draw the polygon generated by the inner circle dots.
        """
        def prep_anim(scene: anim.scene, animator: anim.animator):
            poly = self.inner_polygons[which_inner]
            reveal = anim.reveal_item(poly)
            animator.animate_value(0., 1., self.reveal_duration, reveal)

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
            polys = [self.inter_polygons[which_dot] for which_dot in range(0, self.dots_count)]
            if polys:
                for poly in polys:
                    reveal = anim.reveal_item(poly)
                    animator.animate_value(0., 1., self.reveal_duration, reveal)
            else:
                animator.check_all_anims_done()

        self.add_shots(anim.shot("Draw the inter-circle polygons", "", prep_anim))

    def _anim_all(self):
        """
        Animate all the inner circles and their polygons.
        """
        outer_angle = 360. * self.skip
        inner_angle = 360. * self.inner_count
        def prep_anim(scene: anim.scene, animator: anim.animator):
            for which_inner in range(self.inner_count):
                center = self.inner_centers[which_inner]
                rot_center = anim.rotate_point_around(center, anim.point(0., 0.))
                animator.animate_value(0., outer_angle, 2. * self.animation_speedup, rot_center)
                for which_dot in range(self.dots_count):
                    dot = self.inner_dots_pos[which_inner][which_dot]
                    rot_dot = anim.rotate_point_around(dot, anim.point(0., 0.))
                    animator.animate_value(0., -inner_angle, 2. * self.animation_speedup, rot_dot)

        self.add_shots(anim.shot("Animate all", "", prep_anim))
