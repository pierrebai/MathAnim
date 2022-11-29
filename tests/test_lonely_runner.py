import unittest

from anim import *
from examples.lonely_runner.runners_allowed_intervals import *

class lonely_runner_test(unittest.TestCase):

    def test_gen_runners(self):
        self.assertEqual([], generate_running_runners([], 0))
        self.assertEqual([], generate_running_runners([3], 0))
        self.assertEqual([2], generate_running_runners([1, 3], 0))
        self.assertEqual([2], generate_running_runners([1, 3], 1))
        self.assertEqual([1, 2], generate_running_runners([1, 2, 4], 1))

    def test_runner_intervals(self):
        self.assertEqual([(0.5, 0.5)], generate_one_runner_allowed_time_intervals(1, 2))
        self.assertEqual([(0.25, 0.25), (0.75, 0.75)], generate_one_runner_allowed_time_intervals(2, 2))

        self.assertEqual([(1./3., 1 - 1./3.)], generate_one_runner_allowed_time_intervals(1, 3))
        self.assertEqual([(1./6., 1./2. - 1./6.), (1./2. + 1./6.,  1./2. + (1./2 - 1./6))], generate_one_runner_allowed_time_intervals(2, 3))
