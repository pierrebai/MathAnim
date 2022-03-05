import unittest
import math

from anim import *

dx = 0
dy = 0

def pt(x, y) -> point:
    return point(dx + x, dy + y)

rt2 = math.sqrt(2.)
hrt2 = rt2 / 2.
trt2 = rt2 * 2.
pi = math.pi
hpi = pi / 2.

class geometry_test(unittest.TestCase):

    def test_two_points_angle(self):
        global dx, dy
        dx = dy = 0
        self.assertAlmostEqual( 0.,  two_points_angle(pt(0., 0.), pt( 1.,  0.)))
        self.assertAlmostEqual( hpi, two_points_angle(pt(0., 0.), pt( 0.,  1.)))
        self.assertAlmostEqual( pi,  two_points_angle(pt(0., 0.), pt(-1.,  0.)))
        self.assertAlmostEqual(-hpi, two_points_angle(pt(0., 0.), pt( 0., -1.)))

    def test_four_points_angle(self):
        global dx, dy
        for dx in range(-3, 3):
            for dy in range(-3, 3):
                self.assertAlmostEqual( 0.,  four_points_angle(pt(0., 0.), pt( 0.,  0.), pt(0., 0.), pt( 0.,  0.)))
                self.assertAlmostEqual( 0.,  four_points_angle(pt(0., 0.), pt( 0.,  1.), pt(0., 0.), pt( 0.,  1.)))
                self.assertAlmostEqual( 0.,  four_points_angle(pt(1., 2.), pt( 3.,  4.), pt(1., 2.), pt( 3.,  4.)))

                self.assertAlmostEqual( hpi, four_points_angle(pt(0., 0.), pt( 1.,  0.), pt(0., 0.), pt( 0.,  1.)))
                self.assertAlmostEqual( hpi, four_points_angle(pt(0., 0.), pt( 0.,  1.), pt(0., 0.), pt(-1.,  0.)))
                self.assertAlmostEqual(-pi,  four_points_angle(pt(0., 0.), pt(-1.,  0.), pt(0., 0.), pt( 1.,  0.)))
                self.assertAlmostEqual( hpi, four_points_angle(pt(0., 0.), pt( 0., -1.), pt(0., 0.), pt( 1.,  0.)))

    def test_line_angle(self):
        global dx, dy
        dx = dy = 0
        self.assertAlmostEqual( 0.,  line_angle(line(pt(0., 0.), pt( 1.,  0.))))
        self.assertAlmostEqual( hpi, line_angle(line(pt(0., 0.), pt( 0.,  1.))))
        self.assertAlmostEqual( pi,  line_angle(line(pt(0., 0.), pt(-1.,  0.))))
        self.assertAlmostEqual(-hpi, line_angle(line(pt(0., 0.), pt( 0., -1.))))

    def test_two_lines_angle(self):
        global dx, dy
        for dx in range(-3, 3):
            for dy in range(-3, 3):
                self.assertAlmostEqual( 0.,  two_lines_angle(line(pt(0., 0.), pt( 0.,  0.)), line(pt(0., 0.), pt( 0.,  0.))))
                self.assertAlmostEqual( 0.,  two_lines_angle(line(pt(0., 0.), pt( 0.,  1.)), line(pt(0., 0.), pt( 0.,  1.))))
                self.assertAlmostEqual( 0.,  two_lines_angle(line(pt(1., 2.), pt( 3.,  4.)), line(pt(1., 2.), pt( 3.,  4.))))

                self.assertAlmostEqual( hpi, two_lines_angle(line(pt(0., 0.), pt( 1.,  0.)), line(pt(0., 0.), pt( 0.,  1.))))
                self.assertAlmostEqual( hpi, two_lines_angle(line(pt(0., 0.), pt( 0.,  1.)), line(pt(0., 0.), pt(-1.,  0.))))
                self.assertAlmostEqual(-pi,  two_lines_angle(line(pt(0., 0.), pt(-1.,  0.)), line(pt(0., 0.), pt( 1.,  0.))))
                self.assertAlmostEqual( hpi, two_lines_angle(line(pt(0., 0.), pt( 0., -1.)), line(pt(0., 0.), pt( 1.,  0.))))

    def test_two_points_dot(self):
        global dx, dy
        dx = dy = 0
        self.assertAlmostEqual( 0., two_points_dot(pt(0., 0.), pt( 1.,  0.)))
        self.assertAlmostEqual( 0., two_points_dot(pt(0., 1.), pt( 1.,  0.)))
        self.assertAlmostEqual(-2., two_points_dot(pt(1., 1.), pt(-1., -1.)))
        self.assertAlmostEqual( 1., two_points_dot(pt(0., 1.), pt( 0.,  1.)))
        self.assertAlmostEqual(-1., two_points_dot(pt(1., 0.), pt(-1.,  0.)))
        self.assertAlmostEqual( 2., two_points_dot(pt(0., 1.), pt( 0.,  2.)))

    def test_two_points_sin_dot(self):
        global dx, dy
        dx = dy = 0
        self.assertAlmostEqual( 0., two_points_sin_dot(pt(0., 0.), pt( 1.,  0.)))
        self.assertAlmostEqual( 1., two_points_sin_dot(pt(0., 1.), pt( 1.,  0.)))
        self.assertAlmostEqual( 0., two_points_sin_dot(pt(1., 1.), pt(-1., -1.)))
        self.assertAlmostEqual( 0., two_points_sin_dot(pt(0., 1.), pt( 0.,  1.)))
        self.assertAlmostEqual( 0., two_points_sin_dot(pt(1., 0.), pt(-1.,  0.)))
        self.assertAlmostEqual( 0., two_points_sin_dot(pt(0., 1.), pt( 0.,  2.)))

    def test_two_points_distance(self):
        global dx, dy
        for dx in range(-3, 3):
            for dy in range(-3, 3):
                self.assertAlmostEqual( 1.,   two_points_distance(pt(0., 0.), pt( 1.,  0.)))
                self.assertAlmostEqual( rt2,  two_points_distance(pt(0., 1.), pt( 1.,  0.)))
                self.assertAlmostEqual( trt2, two_points_distance(pt(1., 1.), pt(-1., -1.)))
                self.assertAlmostEqual( 0.,   two_points_distance(pt(0., 1.), pt( 0.,  1.)))
                self.assertAlmostEqual( 2.,   two_points_distance(pt(1., 0.), pt(-1.,  0.)))
                self.assertAlmostEqual( 1.,   two_points_distance(pt(0., 1.), pt( 0.,  2.)))

    def test_delta_distance(self):
        global dx, dy
        for dx in range(-3, 3):
            for dy in range(-3, 3):
                self.assertAlmostEqual( 1.,   delta_distance(pt(0., 0.) - pt( 1.,  0.)))
                self.assertAlmostEqual( rt2,  delta_distance(pt(0., 1.) - pt( 1.,  0.)))
                self.assertAlmostEqual( trt2, delta_distance(pt(1., 1.) - pt(-1., -1.)))
                self.assertAlmostEqual( 0.,   delta_distance(pt(0., 1.) - pt( 0.,  1.)))
                self.assertAlmostEqual( 2.,   delta_distance(pt(1., 0.) - pt(-1.,  0.)))
                self.assertAlmostEqual( 1.,   delta_distance(pt(0., 1.) - pt( 0.,  2.)))

    def test_point_to_two_points_distance(self):
        global dx, dy
        for dx in range(-3, 3):
            for dy in range(-3, 3):
                self.assertAlmostEqual( 0.,   point_to_two_points_distance(pt(0., 0.), pt(0., 0.), pt( 1.,  0.)))
                self.assertAlmostEqual( hrt2, point_to_two_points_distance(pt(0., 0.), pt(0., 1.), pt( 1.,  0.)))
                self.assertAlmostEqual( 0.,   point_to_two_points_distance(pt(0., 0.), pt(1., 1.), pt(-1., -1.)))
                self.assertAlmostEqual( 1.,   point_to_two_points_distance(pt(0., 0.), pt(0., 1.), pt( 0.,  1.)))
                self.assertAlmostEqual( 0.,   point_to_two_points_distance(pt(0., 0.), pt(1., 0.), pt(-1.,  0.)))
                self.assertAlmostEqual( 1.,   point_to_two_points_distance(pt(0., 0.), pt(0., 1.), pt( 0.,  2.)))
                self.assertAlmostEqual( rt2,  point_to_two_points_distance(pt(0., 0.), pt(1., 1.), pt( 1.,  2.)))

    def test_point_to_line_distance(self):
        global dx, dy
        for dx in range(-3, 3):
            for dy in range(-3, 3):
                self.assertAlmostEqual( 0.,   point_to_line_distance(pt(0., 0.), line(pt(0., 0.), pt( 1.,  0.))))
                self.assertAlmostEqual( hrt2, point_to_line_distance(pt(0., 0.), line(pt(0., 1.), pt( 1.,  0.))))
                self.assertAlmostEqual( 0.,   point_to_line_distance(pt(0., 0.), line(pt(1., 1.), pt(-1., -1.))))
                self.assertAlmostEqual( 1.,   point_to_line_distance(pt(0., 0.), line(pt(0., 1.), pt( 0.,  1.))))
                self.assertAlmostEqual( 0.,   point_to_line_distance(pt(0., 0.), line(pt(1., 0.), pt(-1.,  0.))))
                self.assertAlmostEqual( 1.,   point_to_line_distance(pt(0., 0.), line(pt(0., 1.), pt( 0.,  2.))))
                self.assertAlmostEqual( rt2,  point_to_line_distance(pt(0., 0.), line(pt(1., 1.), pt( 1.,  2.))))

    def test_two_points_convex_sum(self):
        global dx, dy
        for dx in range(-3, 3):
            for dy in range(-3, 3):
                self.assertEqual( pt(0.,  0.), two_points_convex_sum(pt(0., 0.), pt( 1.,  0.), 0. ))
                self.assertEqual( pt(1.,  0.), two_points_convex_sum(pt(0., 0.), pt( 1.,  0.), 1. ))
                self.assertEqual( pt(0.5, 0.), two_points_convex_sum(pt(0., 0.), pt( 1.,  0.), 0.5))

    def test_point_to_two_points_projection(self):
        global dx, dy
        for dx in range(-3, 3):
            for dy in range(-3, 3):
                self.assertEqual( pt(0.,  0. ), point_to_two_points_projection(pt(0., 0.), pt(0., 0.), pt( 1.,  0.)))
                self.assertEqual( pt(0.5, 0.5), point_to_two_points_projection(pt(0., 0.), pt(0., 1.), pt( 1.,  0.)))
                self.assertEqual( pt(0.,  0. ), point_to_two_points_projection(pt(0., 0.), pt(1., 1.), pt(-1., -1.)))
                self.assertEqual( pt(0.,  1. ), point_to_two_points_projection(pt(0., 0.), pt(0., 1.), pt( 0.,  1.)))
                self.assertEqual( pt(0.,  0. ), point_to_two_points_projection(pt(0., 0.), pt(1., 0.), pt(-1.,  0.)))
                self.assertEqual( pt(0.,  0. ), point_to_two_points_projection(pt(0., 0.), pt(0., 1.), pt( 0.,  2.)))
                self.assertEqual( pt(1.,  0. ), point_to_two_points_projection(pt(0., 0.), pt(1., 1.), pt( 1.,  2.)))

    def test_two_lines_intersection(self):
        global dx, dy
        for dx in range(-3, 3):
            for dy in range(-3, 3):
                self.assertEqual(pt( 0., 0.), two_lines_intersection(line(pt(-1., 0.), pt(1., 0.)), line(pt( 0., 1.), pt( 0., -1))))
                self.assertEqual(pt( 1., 0.), two_lines_intersection(line(pt(-1., 0.), pt(1., 0.)), line(pt( 1., 1.), pt( 1., -1))))
                self.assertEqual(pt(-1., 0.), two_lines_intersection(line(pt(-1., 0.), pt(1., 0.)), line(pt(-1., 1.), pt(-1., -1))))

                self.assertEqual(pt( 0., 0.), two_lines_intersection(line(pt(-1., -1.), pt(1., 1.)), line(pt( 2., -2.), pt( -2., 2))))

                self.assertIsNone(two_lines_intersection(line(pt(-1., 0.), pt(1., 0.)), line(pt(2., 1.), pt(2., -1))))

    def test_two_lines_intersection_within(self):
        global dx, dy
        for dx in range(-3, 3):
            for dy in range(-3, 3):
                self.assertEqual(pt( 0., 0.), two_lines_intersection_within(line(pt(-1., 0.), pt(1., 0.)), line(pt( 0., 1.), pt( 0., -1))))
                self.assertIsNone(two_lines_intersection_within(line(pt(-1., 0.), pt(1., 0.)), line(pt( 1., 1.), pt( 1., -1))))
                self.assertIsNone(two_lines_intersection_within(line(pt(-1., 0.), pt(1., 0.)), line(pt(-1., 1.), pt(-1., -1))))

                self.assertEqual(pt( 0., 0.), two_lines_intersection_within(line(pt(-1., -1.), pt(1., 1.)), line(pt( 2., -2.), pt( -2., 2))))

                self.assertIsNone(two_lines_intersection_within(line(pt(-1., 0.), pt(1., 0.)), line(pt(2., 1.), pt(2., -1))))

    def test_two_lines_any_intersection(self):
        global dx, dy
        for dx in range(-3, 3):
            for dy in range(-3, 3):
                self.assertEqual(pt( 0., 0.), two_lines_any_intersection(line(pt(-1., 0.), pt(1., 0.)), line(pt( 0., 1.), pt( 0., -1))))
                self.assertEqual(pt( 1., 0.), two_lines_any_intersection(line(pt(-1., 0.), pt(1., 0.)), line(pt( 1., 1.), pt( 1., -1))))
                self.assertEqual(pt(-1., 0.), two_lines_any_intersection(line(pt(-1., 0.), pt(1., 0.)), line(pt(-1., 1.), pt(-1., -1))))

                self.assertEqual(pt( 0., 0.), two_lines_any_intersection(line(pt(-1., -1.), pt(1., 1.)), line(pt( 2., -2.), pt( -2., 2))))

                self.assertEqual(pt( 2., 0.), two_lines_any_intersection(line(pt(-1., 0.), pt(1., 0.)), line(pt(2., 1.), pt(2., -1))))

