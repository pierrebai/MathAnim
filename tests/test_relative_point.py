import unittest

from anim import *


class relative_point_test(unittest.TestCase):

    bases = [
        [ 0., 0.],
        [ 0., 1.],
        [ 1., 0.],
        [ -7., 4.],
        [ -3., -2.],
        [ 5., -3.],
    ]

    def test_relative_point_init(self):
        for bx, by in self.bases:
            base = point(bx, by)

            pt = relative_point(base)
            self.assertAlmostEqual(pt.x(), bx + 0.)
            self.assertAlmostEqual(pt.y(), by + 0.)

            pt = relative_point(base, 2., 3.)
            self.assertAlmostEqual(pt.x(), bx + 2.)
            self.assertAlmostEqual(pt.y(), by + 3.)

            pt2 = relative_point(base, pt)
            self.assertAlmostEqual(pt2.x(), bx + pt.x())
            self.assertAlmostEqual(pt2.y(), by + pt.y())

    def test_set_delta(self):
        for bx, by in self.bases:
            base = point(bx, by)

            pt = relative_point(base, 2., 3.)
            self.assertAlmostEqual(pt.x(), bx + 2.)
            self.assertAlmostEqual(pt.y(), by + 3.)

            pt.set_delta(static_point(5., 6.))
            self.assertAlmostEqual(pt.x(), bx + 5.)
            self.assertAlmostEqual(pt.y(), by + 6.)

    def test_set_origin(self):
        for bx, by in self.bases:
            base = point(bx, by)

            pt = relative_point(base, 2., 3.)
            self.assertAlmostEqual(pt.x(), bx + 2.)
            self.assertAlmostEqual(pt.y(), by + 3.)

            pt.set_origin(point(5., 6.))
            self.assertAlmostEqual(pt.x(), 5. + 2.)
            self.assertAlmostEqual(pt.y(), 6. + 3.)

    def test_set_point(self):
        for bx, by in self.bases:
            base = point(bx, by)

            pt = relative_point(base, 2., 3.)
            self.assertAlmostEqual(pt.x(), bx + 2.)
            self.assertAlmostEqual(pt.y(), by + 3.)

            pt.setX(5.)
            pt.setY(6.)
            self.assertAlmostEqual(pt.x(), 5.)
            self.assertAlmostEqual(pt.y(), 6.)

            pt.set_point(static_point(7., 8.))
            self.assertAlmostEqual(pt.x(), bx + 7.)
            self.assertAlmostEqual(pt.y(), by + 8.)

            pt.set_absolute_point(static_point(1., 6.))
            self.assertAlmostEqual(pt.x(), 1.)
            self.assertAlmostEqual(pt.y(), 6.)

    def test_original_point(self):
        for bx, by in self.bases:
            base = point(bx, by)

            pt = relative_point(base, 2., 3.)
            self.assertAlmostEqual(pt.x(), bx + 2.)
            self.assertAlmostEqual(pt.y(), by + 3.)
            self.assertAlmostEqual(pt.original_point.x(), bx + 2.)
            self.assertAlmostEqual(pt.original_point.y(), by + 3.)

            pt.setX(5.)
            pt.setY(6.)
            self.assertAlmostEqual(pt.x(), 5.)
            self.assertAlmostEqual(pt.y(), 6.)
            self.assertAlmostEqual(pt.original_point.x(), bx + 2.)
            self.assertAlmostEqual(pt.original_point.y(), by + 3.)

            pt.set_point(static_point(7., 8.))
            self.assertAlmostEqual(pt.x(), bx + 7.)
            self.assertAlmostEqual(pt.y(), by + 8.)
            self.assertAlmostEqual(pt.original_point.x(), bx + 2.)
            self.assertAlmostEqual(pt.original_point.y(), by + 3.)

            pt.set_absolute_point(static_point(1., 6.))
            self.assertAlmostEqual(pt.x(), 1.)
            self.assertAlmostEqual(pt.y(), 6.)
            self.assertAlmostEqual(pt.original_point.x(), bx + 2.)
            self.assertAlmostEqual(pt.original_point.y(), by + 3.)

            pt.reset()
            self.assertAlmostEqual(pt.x(), bx + 2.)
            self.assertAlmostEqual(pt.y(), by + 3.)

    def test_distance(self):
        for bx, by in self.bases:
            base = point(bx, by)

            # Expected distance from two relative_points:
            # x1, y1, x2, y2, distance squared, distance from origin squared

            expected = [
                [ 0., 0., 0., 0., 0., 0.],

                [ 0., 0., 1., 0., 1., 0.],
                [ 0., 0., 0., 1., 1., 0.],
                [ 0., 0., 1., 1., 2., 0.],

                [ 1., 0., 0., 0., 1., 1.],
                [ 0., 1., 0., 0., 1., 1.],
                [ 1., 1., 0., 0., 2., 2.],

                [ 1., 2., 3., 5., 13., 5.],
            ]

            for x1, y1, x2, y2, dq, doq in expected:
                doq = (base.x() + x1) ** 2 + (base.y() + y1) ** 2

                p1 = relative_point(base, x1, y1)
                p2 = relative_point(base, x2, y2)
                self.assertAlmostEqual(relative_point.distance_squared(p1, p2), dq)
                self.assertAlmostEqual(relative_point.distance(p1, p2), math.sqrt(dq))
                self.assertAlmostEqual(relative_point.distance_from_origin(p1), math.sqrt(doq))
