from .color import color
from .colors import green, black
from .group import group
from .item import item
from .point import point, static_point, relative_point
from .polygon import polygon
from ..geometry import pi, hpi, tau, four_points_angle, two_points_angle
from ..trf import *
from ..maths import *
from ..algorithms import flatten

from typing import List as _List
from itertools import product

class cube(group):
    """
    A 3D-looking cube made of a group of three polygons.
    The squash factor determines how much face-on the cube is.

    Squash of zero is looking at a corner, squash of one is looking
    almost straight on a face. Defaults is 0.6 which give a nice
    perspective.
    """
    def __init__(self, center: point, radius: float, squash: float = 0.6) -> group:
        self.position = center

        origin = static_point(0., 0.)

        angle_ratio  = 1. - squash
        radius_ratio = 1. - squash / 2.

        # The three point for the main, pale face.
        p5 = origin + static_point(0., radius)
        p6 = p5 + rotate_around_origin(static_point(radius, 0.), -tau * angle_ratio / 12.)
        p1 = static_point(p6.x(), p6.y() - radius)

        # Calculate the center angle of the main face, which
        # dictate how much angle the two other faces have to share,
        # which gives the delta line of the diagonal line going out of
        # the corner of teh main face to make the common edge of the
        # two other faces:
        #
        #       \  <- diagonal
        #        \_____
        #        |     |  <- main face (actually at a slight angle)
        #        |_____|

        center_angle = four_points_angle(origin, p5, origin, p1)
        top_angle = two_points_angle(origin, p1)
        delta = rotate_around_origin(static_point(radius * radius_ratio, 0.), top_angle + (tau - center_angle) / 2.)

        p2 = p1 + delta
        p4 = p5 + delta
        p3 = static_point(p4.x(), p4.y() - radius)

        cube_center = relative_point(center, origin)
        hexagon_pts = [p1, p2, p3, p4, p5, p6, p1]
        hexagon_pts = [relative_point(center, pt) for pt in hexagon_pts]

        polys_pts = [hexagon_pts[i*2:i*2+3] + [cube_center] for i in range(3)]
        polys = [polygon(pts).outline(black) for pts in polys_pts]
        super().__init__(polys)
        self.fill(green)

    def fill(self, fill_color: color):
        """
        Sets the color used to fill the item.
        """
        colors = [fill_color, fill_color.darker(130), fill_color.lighter(130)]
        for poly, color in zip(self.sub_items, colors):
            poly.fill(color)
        return self

    def get_deltas(self) -> _List[static_point]:
        """
        Retrieve the delta movements to adjoin another identical cube to this cube
        when moving in the 3D x, y and z directions.
        """
        dx = self.sub_items[2].points[1] - self.sub_items[2].points[0]
        dy = self.sub_items[0].points[2] - self.sub_items[0].points[-1]
        dz = self.sub_items[2].points[0] - self.sub_items[2].points[-1]
        return [dx, dy, dz]

class cube_of_cubes(group):
    """
    Create a cube (or rectangular prism) made of cubes.
    """
    def __init__(self, sizes: int|_List[int], center: point, radius: float, squash: float = 0.):
        """
        Create a rectangular prism. If the sizes is a single value, then a cube is made.
        """
        dx, dy, dz = static_point(0., 0.), static_point(0., 0.), static_point(0., 0.)
        order = 0.
        x_cubes = []

        if isinstance(sizes, int):
            sizes = [sizes]
        elif not sizes:
            sizes = [1]
        while len(sizes) < 3:
            sizes.append(sizes[-1])
        sizes = [max(size, 1) for size in sizes[0:3]]

        for x in range(sizes[0]):
            y_cubes = []
            for y in range(sizes[1]):
                z_cubes = []
                for z in range(sizes[2]):
                    cube_center = relative_point(center, dx * x + dy * y + dz * z)
                    new_cube = cube(cube_center, radius, squash).set_z_order(order)
                    z_cubes.append(new_cube)
                    if not order:
                        dx, dy, dz = new_cube.get_deltas()
                    order -= 1.
                y_cubes.append(z_cubes)
            x_cubes.append(y_cubes)
        self.cubes = x_cubes
        self.sizes = sizes
        super().__init__(flatten(x_cubes))

    def get_deltas(self) -> _List[static_point]:
        """
        Retrieve the delta movements to adjoin two inner cubes
        when moving in the 3D x, y and z directions.
        """
        return self.sub_items[0].get_deltas()

    def get_whole_deltas(self) -> _List[static_point]:
        """
        Retrieve the delta movements to adjoin identical cube of cubes
        when moving in the 3D x, y and z directions.
        """
        return [delta * size for delta, size in zip(self.get_deltas(), self.sizes)]

    def get_x_slices(self) -> _List[_List[_List[cube]]]:
        """
        Return a list of array of slices of the cube, sliced along the X axis.
        """
        return self.cubes

    def get_y_slices(self)-> _List[_List[_List[cube]]]:
        """
        Return a list of array of slices of the cube, sliced along the Y axis.
        """
        y_cubes = []
        for y in range(self.sizes[1]):
            x_cubes = []
            for x in range(self.sizes[0]):
                z_cubes = []
                for z in range(self.sizes[2]):
                    z_cubes.append(self.cubes[x][y][z])
                x_cubes.append(z_cubes)
            y_cubes.append(x_cubes)
        return y_cubes

    def get_z_slices(self)-> _List[_List[_List[cube]]]:
        """
        Return a list of array of slices of the cube, sliced along the Z axis.
        """
        z_cubes = []
        for z in range(self.sizes[2]):
            x_cubes = []
            for x in range(self.sizes[0]):
                y_cubes = []
                for y in range(self.sizes[1]):
                    y_cubes.append(self.cubes[x][y][z])
                x_cubes.append(y_cubes)
            z_cubes.append(x_cubes)
        return z_cubes
