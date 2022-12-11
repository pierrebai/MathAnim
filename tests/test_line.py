import unittest

from anim import *

class line_test(unittest.TestCase):

    def test_init(self):
        p1 = point(0., 0.)
        p2 = point(0., 0.)
        l = line(p1, p2)

        self.assertEqual(l.p1, p1)
        self.assertEqual(l.p2, p2)
        self.assertEqual(l.length(), 0.)
        self.assertListEqual(l.get_all_points(), [p1, p2])

        p1 = point(-1., 1.)
        p2 = point(3., -2.)
        l = line(p1, p2)

        self.assertEqual(l.p1, p1)
        self.assertEqual(l.p2, p2)
        self.assertAlmostEqual(l.length(), 5.)
        self.assertListEqual(l.get_all_points(), [p1, p2])
