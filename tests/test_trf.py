import unittest

from anim import *
from anim.trf import *

dx = 0
dy = 0

def pt(x, y) -> point:
    return point(dx + x, dy + y)

class trf_test(unittest.TestCase):

    def test_rotate_around(self):
        global dx, dy
        for dx in range(-3, 3):
            for dy in range(-3, 3):
                delta = pt(0., 10.) - rotate_around(pt(10., 0.), pt(0., 0.), math.pi / 2.)
                self.assertAlmostEqual(0., delta.x())
                self.assertAlmostEqual(0., delta.y())

    def test_rotate_around_origin(self):
        global dx, dy
        dx = dy = 0.
        delta = pt(0., 10.) - rotate_around_origin(pt(10., 0.), math.pi / 2.)
        self.assertAlmostEqual(0., delta.x())
        self.assertAlmostEqual(0., delta.y())
