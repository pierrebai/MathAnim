from .point import point, relative_point
from .rectangle import static_rectangle
from .item import item

import math
from typing import Tuple as _Tuple, List as _List

from PySide6.QtWidgets import QGraphicsEllipseItem as _QGraphicsEllipseItem
from PySide6.QtCore import QRectF as _QRectF

class _circle_base(_QGraphicsEllipseItem, item):
    """
    A circle item that is dynamically updated when points defining it move.
    """
    def __init__(self):
        super().__init__(None)

    def get_center_and_radius(self, center: point, radius: float) -> _Tuple[relative_point, float]:
        """
        Retrieves the center and radius.
        """
        pass

    def get_circumference_point(self, radian_angle: float) -> relative_point:
        """
        Creates a relative point on the circle circumference.
        """
        center, radius = self.get_center_and_radius()
        dx = math.cos(radian_angle) * radius
        dy = math.sin(radian_angle) * radius
        return relative_point(center, dx, dy)

    def scene_rect(self) -> static_rectangle:
        return self.sceneBoundingRect()        

    def _update_geometry(self):
        """
        Updates the circle geometry if the rectangle changed.
        """
        center, radius = self.get_center_and_radius()
        diameter = radius * 2.0
        current_rect = _QRectF(center.x() - radius, center.y() - radius, diameter, diameter)
        if current_rect != self.rect():
            self.prepareGeometryChange()
            self.setRect(current_rect)


class circle(_circle_base):
    """
    A circle item that is dynamically updated when the center-point or radius move.
    """
    def __init__(self, center: point, radius: float):
        super().__init__()
        self.center = center
        self.radius = radius
        center.add_user(self)
        self._update_geometry()

    def set_center(self, new_center: point) -> _circle_base:
        if self.center:
            self.center.remove_user(self)
        self.center = new_center
        new_center.add_user(self)
        return self

    def set_radius(self, new_radius) -> _circle_base:
        if new_radius != self.radius:
            self.radius = new_radius
            self._update_geometry()
        return self

    def get_center_and_radius(self):
        """
        Retrieves the center and radius.
        """
        return (self.center, self.radius)

    def get_all_points(self) -> _List[point]:
        """
        Retrieve all animatable points in the item.
        """
        return [self.center]


class diameter_circle(_circle_base):
    """
    A circle item that is dynamically updated when its diameter end-points move.
    """
    def __init__(self, diam_p1: point, diam_p2: point):
        super().__init__()
        self.diameter_p1 = diam_p1
        self.diameter_p2 = diam_p2
        diam_p1.add_user(self)
        diam_p2.add_user(self)
        self._update_geometry()

    def get_center_and_radius(self):
        """
        Retrieves the center and radius.
        The center is relative to p1.
        """
        p1 = self.diameter_p1
        p2 = self.diameter_p2
        center = relative_point(p1, (p2 - p1) * 0.5)
        dx2 = (center.x() - p2.x()) ** 2
        dy2 = (center.y() - p2.y()) ** 2
        radius = math.sqrt(dx2 + dy2)

        return (center, radius)

    def get_all_points(self) -> _List[point]:
        """
        Retrieve all animatable points in the item.
        """
        return [self.diameter_p1, self.diameter_p2]


class radius_circle(_circle_base):
    """
    A circle item that is dynamically updated when its radius end-points move.
    """
    def __init__(self, center: point, radius_point: point):
        super().__init__()
        self.center = center
        self.radius_point = radius_point
        center.add_user(self)
        radius_point.add_user(self)
        self._update_geometry()

    def set_radius(self, radius_point: point) -> _circle_base:
        if self.radius_point:
            self.radius_point.remove_user(self)
        self.radius_point = radius_point
        radius_point.add_user(self)
        return self

    def set_center(self, new_center: point) -> _circle_base:
        if self.center:
            self.center.remove_user(self)
        self.center = new_center
        new_center.add_user(self)
        return self

    def get_center_and_radius(self):
        """
        Retrieves the center and radius.
        """
        center = self.center
        rad_pt = self.radius_point
        dx2 = (center.x() - rad_pt.x()) ** 2
        dy2 = (center.y() - rad_pt.y()) ** 2
        radius = math.sqrt(dx2 + dy2)

        return (center, radius)

    def get_all_points(self) -> _List[point]:
        """
        Retrieve all animatable points in the item.
        """
        return [self.center, self.radius_point]
