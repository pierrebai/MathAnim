import unittest

from anim import *

class types_test(unittest.TestCase):

    def test_is_of_type(self):
        self.assertTrue(is_of_type('', str))
        self.assertTrue(is_of_type([''], str))
        self.assertTrue(is_of_type(([''],), str))

        self.assertTrue(is_of_type(1., float))
        self.assertTrue(is_of_type((1.,), float))
        self.assertTrue(is_of_type([(1.,)], float))

        self.assertTrue(is_of_type(point(), static_point))
        self.assertFalse(is_of_type(static_point(), point))

        self.assertFalse(is_of_type([], float))
        self.assertFalse(is_of_type(None, float))
        self.assertFalse(is_of_type('', float))

    def test_flatten(self):
        self.assertEqual([], flatten([]))
        self.assertEqual([1], flatten([1]))
        self.assertEqual([1], flatten([[[1]]]))        
        self.assertEqual([1, 2, 3], flatten([[[1, 2, 3]]]))
        self.assertEqual([1, 2, 3], flatten([[[1], 2], 3]))

    def test_find_all_of_type(self):
        a = 1
        b = ''
        c = point()
        self.assertEqual([a], find_all_of_type(locals(), int))
        self.assertEqual([b], find_all_of_type(locals(), str))
        self.assertEqual([c], find_all_of_type(locals(), point))
        self.assertEqual([c], find_all_of_type(locals(), static_point))
        self.assertEqual([], find_all_of_type(locals(), float))
