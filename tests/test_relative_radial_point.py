import unittest

from anim import *


class relative_radial_point_test(unittest.TestCase):

    # Radius, angle
    bases = [
        [ 0., 0.],
        [ 2., 0.],
        [ 2., pi / 3.],
        [ 4., pi / 6.],
    ]

    def test_relative_radial_point_init(self):
        # Radius, angle
        radius_angle_deltas = [
            [2, pi / 3. ],
        ]

        for radius, angle in radius_angle_deltas:
            for br, ba in self.bases:
                with self.subTest(f'r {radius} - a {round(360 * angle / tau)} - br {br} - ba {round(360 * ba / tau)}'):
                    base = radial_point(point(0., 0.), br, ba)

                    total_radius = 0. + br
                    total_angle  = 0.  + ba
                    ex = cos(total_angle) * total_radius
                    ey = sin(total_angle) * total_radius

                    pt = relative_radial_point(base, 0., 0.)
                    self.assertAlmostEqual(pt.x(), ex)
                    self.assertAlmostEqual(pt.y(), ey)

                    total_radius = radius + br
                    total_angle  = angle  + ba
                    ex = cos(total_angle) * total_radius
                    ey = sin(total_angle) * total_radius

                    pt = relative_radial_point(base, radius, angle)
                    self.assertAlmostEqual(pt.x(), ex)
                    self.assertAlmostEqual(pt.y(), ey)

    def test_set_radius_delta(self):
        # Radius, angle
        radius_angle_deltas = [
            [2, pi / 3. ],
        ]

        for radius, angle in radius_angle_deltas:
            for br, ba in self.bases:
                with self.subTest(f'r {radius} - a {round(360 * angle / tau)} - br {br} - ba {round(360 * ba / tau)}'):
                    base = radial_point(point(0., 0.), br, ba)

                    total_radius = radius + br
                    total_angle  = angle  + ba
                    ex = cos(total_angle) * total_radius
                    ey = sin(total_angle) * total_radius

                    pt = relative_radial_point(base, radius, angle)
                    self.assertAlmostEqual(pt.x(), ex)
                    self.assertAlmostEqual(pt.y(), ey)

                    total_radius = 5. + br
                    ex = cos(total_angle) * total_radius
                    ey = sin(total_angle) * total_radius

                    pt.set_radius_delta(5.)
                    self.assertAlmostEqual(pt.x(), ex)
                    self.assertAlmostEqual(pt.y(), ey)

    def test_set_angle_delta(self):
        # Radius, angle
        radius_angle_deltas = [
            [2, pi / 3. ],
        ]

        for radius, angle in radius_angle_deltas:
            for br, ba in self.bases:
                with self.subTest(f'r {radius} - a {round(360 * angle / tau)} - br {br} - ba {round(360 * ba / tau)}'):
                    base = radial_point(point(0., 0.), br, ba)

                    total_radius = radius + br
                    total_angle  = angle  + ba
                    ex = cos(total_angle) * total_radius
                    ey = sin(total_angle) * total_radius

                    pt = relative_radial_point(base, radius, angle)
                    self.assertAlmostEqual(pt.x(), ex)
                    self.assertAlmostEqual(pt.y(), ey)

                    total_radius = radius + br
                    total_angle  = pi / 6.  + ba
                    ex = cos(total_angle) * total_radius
                    ey = sin(total_angle) * total_radius

                    pt.set_angle_delta(pi / 6.)
                    self.assertAlmostEqual(pt.x(), ex)
                    self.assertAlmostEqual(pt.y(), ey)

    def test_set_origin(self):
        # Radius, angle
        radius_angle_deltas = [
            [2, pi / 3. ],
        ]

        for radius, angle in radius_angle_deltas:
            for br, ba in self.bases:
                with self.subTest(f'r {radius} - a {round(360 * angle / tau)} - br {br} - ba {round(360 * ba / tau)}'):
                    base = radial_point(point(0., 0.), br, ba)

                    total_radius = radius + br
                    total_angle  = angle  + ba
                    ex = cos(total_angle) * total_radius
                    ey = sin(total_angle) * total_radius

                    pt = relative_radial_point(base, radius, angle)
                    self.assertAlmostEqual(pt.x(), ex)
                    self.assertAlmostEqual(pt.y(), ey)

                    total_radius = radius + 3.
                    total_angle  = angle  + pi
                    ex = cos(total_angle) * total_radius
                    ey = sin(total_angle) * total_radius

                    pt.set_origin(radial_point(point(0., 0.), 3., pi))
                    self.assertAlmostEqual(pt.x(), ex)
                    self.assertAlmostEqual(pt.y(), ey)

    def test_set_point(self):
        # Radius, angle
        radius_angle_deltas = [
            [2, pi / 3. ],
        ]

        for radius, angle in radius_angle_deltas:
            for br, ba in self.bases:
                with self.subTest(f'r {radius} - a {round(360 * angle / tau)} - br {br} - ba {round(360 * ba / tau)}'):
                    base = radial_point(point(0., 0.), br, ba)

                    total_radius = radius + br
                    total_angle  = angle  + ba
                    ex = cos(total_angle) * total_radius
                    ey = sin(total_angle) * total_radius

                    pt = relative_radial_point(base, radius, angle)
                    self.assertAlmostEqual(pt.x(), ex)
                    self.assertAlmostEqual(pt.y(), ey)

                    pt.setX(5.)
                    pt.setY(6.)
                    self.assertAlmostEqual(pt.x(), 5.)
                    self.assertAlmostEqual(pt.y(), 6.)

                    nrd = sqrt(7 ** 2 + 8 **2)
                    nad = atan2(8., 7.)
                    total_radius = nrd + br
                    total_angle  = nad + ba
                    nx = cos(total_angle) * total_radius
                    ny = sin(total_angle) * total_radius

                    pt.set_point(static_point(7., 8.))
                    self.assertAlmostEqual(pt.x(), nx)
                    self.assertAlmostEqual(pt.y(), ny)
                    self.assertAlmostEqual(pt.radius_delta, nrd)
                    self.assertAlmostEqual(pt.angle_delta, nad)

                    nrd = sqrt(1 ** 2 + 6 **2) - br
                    nad = atan2(6., 1.) - ba

                    pt.set_absolute_point(static_point(1., 6.))
                    self.assertAlmostEqual(pt.x(), 1.)
                    self.assertAlmostEqual(pt.y(), 6.)
                    self.assertAlmostEqual(pt.radius_delta, nrd)
                    self.assertAlmostEqual(pt.angle_delta, nad)

    def test_original_point(self):
        # Radius, angle
        radius_angle_deltas = [
            [2, pi / 3. ],
        ]

        for radius, angle in radius_angle_deltas:
            for br, ba in self.bases:
                with self.subTest(f'r {radius} - a {round(360 * angle / tau)} - br {br} - ba {round(360 * ba / tau)}'):
                    base = radial_point(point(0., 0.), br, ba)

                    total_radius = radius + br
                    total_angle  = angle  + ba
                    ex = cos(total_angle) * total_radius
                    ey = sin(total_angle) * total_radius

                    pt = relative_radial_point(base, radius, angle)
                    self.assertAlmostEqual(pt.x(), ex)
                    self.assertAlmostEqual(pt.y(), ey)
                    self.assertAlmostEqual(pt.original_point.x(), ex)
                    self.assertAlmostEqual(pt.original_point.y(), ey)

                    pt.setX(5.)
                    pt.setY(6.)
                    self.assertAlmostEqual(pt.x(), 5.)
                    self.assertAlmostEqual(pt.y(), 6.)
                    self.assertAlmostEqual(pt.original_point.x(), ex)
                    self.assertAlmostEqual(pt.original_point.y(), ey)

                    total_radius = sqrt(7 ** 2 + 8 **2) + br
                    total_angle  = atan2(8., 7.) + ba
                    nx = cos(total_angle) * total_radius
                    ny = sin(total_angle) * total_radius

                    pt.set_point(static_point(7., 8.))
                    self.assertAlmostEqual(pt.x(), nx)
                    self.assertAlmostEqual(pt.y(), ny)
                    self.assertAlmostEqual(pt.original_point.x(), ex)
                    self.assertAlmostEqual(pt.original_point.y(), ey)

                    pt.set_absolute_point(static_point(1., 6.))
                    self.assertAlmostEqual(pt.x(), 1.)
                    self.assertAlmostEqual(pt.y(), 6.)
                    self.assertAlmostEqual(pt.original_point.x(), ex)
                    self.assertAlmostEqual(pt.original_point.y(), ey)

                    pt.reset()
                    self.assertAlmostEqual(pt.x(), ex)
                    self.assertAlmostEqual(pt.y(), ey)
                    self.assertAlmostEqual(pt.radius_delta, radius)
                    self.assertAlmostEqual(pt.angle_delta, angle)
