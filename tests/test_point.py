import unittest

from anim import *


class point_test(unittest.TestCase):

    def test_point_init(self):
        pt = point()
        self.assertAlmostEqual(pt.x(), 0.)
        self.assertAlmostEqual(pt.y(), 0.)

        pt = point(2., 3.)
        self.assertAlmostEqual(pt.x(), 2.)
        self.assertAlmostEqual(pt.y(), 3.)

        pt2 = point(pt)
        self.assertAlmostEqual(pt2.x(), 2.)
        self.assertAlmostEqual(pt2.y(), 3.)

    def test_set_point(self):
        pt = point(2., 3.)
        self.assertAlmostEqual(pt.x(), 2.)
        self.assertAlmostEqual(pt.y(), 3.)

        pt.setX(5.)
        pt.setY(6.)
        self.assertAlmostEqual(pt.x(), 5.)
        self.assertAlmostEqual(pt.y(), 6.)

        pt.set_point(static_point(7., 8.))
        self.assertAlmostEqual(pt.x(), 7.)
        self.assertAlmostEqual(pt.y(), 8.)

        pt.set_absolute_point(static_point(1., 6.))
        self.assertAlmostEqual(pt.x(), 1.)
        self.assertAlmostEqual(pt.y(), 6.)

    def test_original_point(self):
        pt = point(2., 3.)
        self.assertAlmostEqual(pt.x(), 2.)
        self.assertAlmostEqual(pt.y(), 3.)
        self.assertAlmostEqual(pt.original_point.x(), 2.)
        self.assertAlmostEqual(pt.original_point.y(), 3.)

        pt.setX(5.)
        pt.setY(6.)
        self.assertAlmostEqual(pt.x(), 5.)
        self.assertAlmostEqual(pt.y(), 6.)
        self.assertAlmostEqual(pt.original_point.x(), 2.)
        self.assertAlmostEqual(pt.original_point.y(), 3.)

        pt.set_point(static_point(7., 8.))
        self.assertAlmostEqual(pt.x(), 7.)
        self.assertAlmostEqual(pt.y(), 8.)
        self.assertAlmostEqual(pt.original_point.x(), 2.)
        self.assertAlmostEqual(pt.original_point.y(), 3.)

        pt.set_absolute_point(static_point(1., 6.))
        self.assertAlmostEqual(pt.x(), 1.)
        self.assertAlmostEqual(pt.y(), 6.)
        self.assertAlmostEqual(pt.original_point.x(), 2.)
        self.assertAlmostEqual(pt.original_point.y(), 3.)

        pt.reset()
        self.assertAlmostEqual(pt.x(), 2.)
        self.assertAlmostEqual(pt.y(), 3.)

    def test_distance(self):
        # Expected distance from two points:
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
            p1 = point(x1, y1)
            p2 = point(x2, y2)
            self.assertAlmostEqual(point.distance_squared(p1, p2), dq)
            self.assertAlmostEqual(point.distance(p1, p2), math.sqrt(dq))
            self.assertAlmostEqual(point.distance_from_origin(p1), math.sqrt(doq))
