import unittest

from anim import *


class radial_point_test(unittest.TestCase):

    bases = [
        [ 0., 0.],
        [ 0., 1.],
        [ 1., 0.],
        [ -7., 4.],
        [ -3., -2.],
        [ 5., -3.],
    ]

    def test_radial_point_init(self):
        # Radius, angle, resulting delta x and y
        radius_angle_deltas = [
            [2, pi / 3., 1., sqrt(3) ],
        ]

        for radius, angle, dx, dy in radius_angle_deltas:
            for bx, by in self.bases:
                base = point(bx, by)

                pt = radial_point(base, 0., angle)
                self.assertAlmostEqual(pt.x(), bx + 0.)
                self.assertAlmostEqual(pt.y(), by + 0.)

                pt = radial_point(base, radius, angle)
                self.assertAlmostEqual(pt.x(), bx + dx)
                self.assertAlmostEqual(pt.y(), by + dy)

    def test_set_radius(self):
        # Radius, angle, resulting delta x and y
        radius_angle_deltas = [
            [2, pi / 3., 1., sqrt(3) ],
        ]

        for radius, angle, dx, dy in radius_angle_deltas:
            for bx, by in self.bases:
                base = point(bx, by)

                pt = radial_point(base, radius, angle)
                self.assertAlmostEqual(pt.x(), bx + dx)
                self.assertAlmostEqual(pt.y(), by + dy)

                pt.set_radius(5.)
                self.assertAlmostEqual(pt.x(), bx + dx * 5 / radius)
                self.assertAlmostEqual(pt.y(), by + dy * 5 / radius)

    def test_set_angle(self):
        # Radius, angle, resulting delta x and y
        radius_angle_deltas = [
            [2, pi / 3., 1., sqrt(3) ],
        ]

        for radius, angle, dx, dy in radius_angle_deltas:
            for bx, by in self.bases:
                base = point(bx, by)

                pt = radial_point(base, radius, angle)
                self.assertAlmostEqual(pt.x(), bx + dx)
                self.assertAlmostEqual(pt.y(), by + dy)

                # Note: going from 60 to 30 degrees invert the dx and dy
                pt.set_angle(pi / 6.)
                self.assertAlmostEqual(pt.x(), bx + dy)
                self.assertAlmostEqual(pt.y(), by + dx)

    def test_set_origin(self):
        # Radius, angle, resulting delta x and y
        radius_angle_deltas = [
            [2, pi / 3., 1., sqrt(3) ],
        ]

        for radius, angle, dx, dy in radius_angle_deltas:
            for bx, by in self.bases:
                base = point(bx, by)

                pt = radial_point(base, radius, angle)
                self.assertAlmostEqual(pt.x(), bx + dx)
                self.assertAlmostEqual(pt.y(), by + dy)

                pt.set_origin(point(5., 6.))
                self.assertAlmostEqual(pt.x(), 5. + dx)
                self.assertAlmostEqual(pt.y(), 6. + dy)

    def test_set_point(self):
        # Radius, angle, resulting delta x and y
        radius_angle_deltas = [
            [2, pi / 3., 1., sqrt(3) ],
        ]

        for radius, angle, dx, dy in radius_angle_deltas:
            for bx, by in self.bases:
                base = point(bx, by)

                pt = radial_point(base, radius, angle)
                self.assertAlmostEqual(pt.x(), bx + dx)
                self.assertAlmostEqual(pt.y(), by + dy)

                pt.setX(5.)
                pt.setY(6.)
                self.assertAlmostEqual(pt.x(), 5.)
                self.assertAlmostEqual(pt.y(), 6.)

                pt.set_point(static_point(7., 8.))
                self.assertAlmostEqual(pt.x(), bx + 7.)
                self.assertAlmostEqual(pt.y(), by + 8.)
                # TODO: should assert on new angle and radius

                pt.set_absolute_point(static_point(1., 6.))
                self.assertAlmostEqual(pt.x(), 1.)
                self.assertAlmostEqual(pt.y(), 6.)
                # TODO: should assert on new angle and radius

    def test_original_point(self):
        # Radius, angle, resulting delta x and y
        radius_angle_deltas = [
            [2, pi / 3., 1., sqrt(3) ],
        ]

        for radius, angle, dx, dy in radius_angle_deltas:
            for bx, by in self.bases:
                base = point(bx, by)

                pt = radial_point(base, radius, angle)
                self.assertAlmostEqual(pt.x(), bx + dx)
                self.assertAlmostEqual(pt.y(), by + dy)
                self.assertAlmostEqual(pt.original_point.x(), bx + dx)
                self.assertAlmostEqual(pt.original_point.y(), by + dy)

                pt.setX(5.)
                pt.setY(6.)
                self.assertAlmostEqual(pt.x(), 5.)
                self.assertAlmostEqual(pt.y(), 6.)
                self.assertAlmostEqual(pt.original_point.x(), bx + dx)
                self.assertAlmostEqual(pt.original_point.y(), by + dy)

                pt.set_point(static_point(7., 8.))
                self.assertAlmostEqual(pt.x(), bx + 7.)
                self.assertAlmostEqual(pt.y(), by + 8.)
                self.assertAlmostEqual(pt.original_point.x(), bx + dx)
                self.assertAlmostEqual(pt.original_point.y(), by + dy)

                pt.set_absolute_point(static_point(1., 6.))
                self.assertAlmostEqual(pt.x(), 1.)
                self.assertAlmostEqual(pt.y(), 6.)
                self.assertAlmostEqual(pt.original_point.x(), bx + dx)
                self.assertAlmostEqual(pt.original_point.y(), by + dy)

                pt.reset()
                self.assertAlmostEqual(pt.x(), bx + dx)
                self.assertAlmostEqual(pt.y(), by + dy)
