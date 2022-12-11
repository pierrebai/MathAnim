from PySide6.QtCore import QPointF as _QPointF
from typing import List as _List, Callable as _Callable
from math import cos as _cos, sin as _sin, sqrt as _sqrt, atan2 as _atan2

static_point= _QPointF
    
class point(static_point):
    """
    A dynamic point that can be animated from its original position and which
    propagates its movement to dynamic items built from it.
    """

    def __init__(self, *args) -> None:
        if len(args) == 0:
            x = 0
            y = 0
        elif len(args) == 1:
            x = args[0].x()
            y = args[0].y()
        else:
            x = args[0]
            y = args[1]
        super().__init__(x, y)
        self._start_pos = static_point(x, y)
        self._users = []

    @property
    def original_point(self) -> static_point:
        """
        The original position of the point, useful to animate from the starting position.
        """
        return self._start_pos

    def add_user(self, user) -> static_point:
        """
        Adds a user of the popint that will be notified when the point moves.
        """
        self._users.append(user)
        return self

    def remove_user(self, user) -> static_point:
        """
        Removes a user of the popint that was notified when the point moved.
        """
        self._users.remove(user)
        return self

    def set_point(self, new_point: static_point) -> static_point:
        """
        Updates the point position and notifies its users.
        """
        if self != new_point:
            self.setX(new_point.x())
            self.setY(new_point.y())

            for u in self._users:
                u._update_geometry()
        return self

    def set_absolute_point(self, new_point: static_point) -> static_point:
        """
        Updates the point absolute position and notifies its users.
        """
        self.set_point(new_point)
        return self

    def reset(self) -> static_point:
        """
        Resets the point to its original location.
        """
        self.set_absolute_point(self.original_point)
        return self

    @staticmethod
    def distance_squared(p1: static_point, p2: static_point) -> float:
        """
        Returns the square of the distance between two points.
        This is used when only relative distance need to be compared,
        avoiding a square root.
        """
        delta = p1 - p2
        return delta.x() ** 2 + delta.y() ** 2

    @staticmethod
    def distance(p1: static_point, p2: static_point) -> float:
        """
        Returns the distance between two points.
        """
        return _sqrt(point.distance_squared(p1, p2))

    @staticmethod
    def distance_from_origin(p1: static_point) -> float:
        """
        Returns the distance between two points.
        """
        return _sqrt(point.distance_squared(p1, static_point(0., 0.)))

class relative_point(point):
    """
    A dynamic point with an position relative to another point, called its origin.
    """

    def __init__(self, origin: point, *args) -> None:
        super().__init__(*args)
        self.origin = None
        self.delta = static_point(self._start_pos)
        self.original_delta = self.delta
        self.set_origin(origin)
        self._start_pos = static_point(self)

    def set_delta(self, new_delta: static_point) -> point:
        if self.delta != new_delta:
            self.delta = new_delta
            self._update_geometry()
        return self

    def set_origin(self, new_origin: point) -> point:
        """
        Sets this relative point to be relative to a new origin.
        """
        if self.origin:
            self.origin.remove_user(self)
        self.origin = new_origin
        new_origin.add_user(self)
        self._update_geometry()
        return self

    def _update_geometry(self) -> None:
        """
        Updates the point position relative to its origin when the point it is relative to has moved.
        """
        new_pos = self.origin + self.delta
        if new_pos != self:
            super().set_point(new_pos)

    def set_point(self, new_point: static_point) -> point:
        """
        Updates the point position relative to its origin and notifies its users.
        """
        self.delta = static_point(new_point)
        self._update_geometry()
        return self

    def set_absolute_point(self, new_point: static_point) -> point:
        """
        Updates the point absolute position and notifies its users.
        """
        self.delta = new_point - self.origin
        self._update_geometry()
        return self

class radial_point(point):
    """
    A dynamic point with an position at given distance and angle around from another point, called its origin.
    """

    def __init__(self, origin: point, radius: float, angle: float, *args) -> None:
        super().__init__(*args)
        self.origin = None
        self.radius = radius
        self.angle = angle
        self.set_origin(origin)
        self._start_pos = static_point(self)

    def set_angle(self, new_angle: float) -> point:
        if self.angle != new_angle:
            self.angle = new_angle
            self._update_geometry()
        return self

    def set_radius(self, new_radius: float) -> point:
        if self.radius != new_radius:
            self.radius = new_radius
            self._update_geometry()
        return self

    def set_origin(self, new_origin: point) -> point:
        """
        Sets this relative point to be relative to a new origin.
        """
        if self.origin:
            self.origin.remove_user(self)
        self.origin = new_origin
        new_origin.add_user(self)
        self._update_geometry()
        return self

    def _update_geometry(self) -> None:
        """
        Updates the point position relative to its origin when the point it is relative to has moved.
        """
        new_pos = self._calculate_position(self.radius, self.angle)
        if new_pos != self:
            super().set_point(new_pos)

    def _calculate_position(self, radius: float, angle: float) -> None:
        """
        Updates the point position relative to its origin when the point it is relative to has moved.
        """
        return self.origin + static_point(_cos(angle), _sin(angle)) * radius

    def set_point(self, new_point: static_point) -> point:
        """
        Updates the point position relative to its origin and notifies its users.
        """
        self.radius = point.distance(new_point, static_point(0., 0.))
        self.angle = _atan2(new_point.y(), new_point.x())
        self._update_geometry()
        return self

    def set_absolute_point(self, new_point: static_point) -> point:
        """
        Updates the point absolute position and notifies its users.
        """
        self.radius = point.distance(self.origin, new_point)
        self.angle = _atan2(new_point.y() - self.origin.y(), new_point.x() - self.origin.x())
        self._update_geometry()
        return self


class relative_radial_point(point):
    """
    A dynamic point with an position an angle away from another radial point, called its origin.
    """

    def __init__(self, origin: radial_point, radius_delta: float, angle_delta: float, *args) -> None:
        super().__init__(*args)
        self.radius_delta = radius_delta
        self.angle_delta = angle_delta
        self.origin: radial_point = None
        self.set_origin(origin)
        self._start_pos = static_point(self)

    def set_origin(self, new_origin: radial_point) -> point:
        """
        Sets this relative point to be relative to a new origin.
        """
        if self.origin:
            self.origin.remove_user(self)
        self.origin = new_origin
        new_origin.add_user(self)
        self._update_geometry()
        return self

    def set_radius_delta(self, new_delta: float) -> point:
        if self.radius_delta != new_delta:
            self.radius_delta = new_delta
            self._update_geometry()
        return self

    def set_angle_delta(self, new_delta: float) -> point:
        if self.angle_delta != new_delta:
            self.angle_delta = new_delta
            self._update_geometry()
        return self

    def _update_geometry(self) -> None:
        """
        Updates the point position relative to its origin when the point it is relative to has moved.
        """
        new_pos = self.origin._calculate_position(self.origin.radius + self.radius_delta, self.origin.angle + self.angle_delta)
        if new_pos != self:
            super().set_point(new_pos)

    def set_point(self, new_point: static_point) -> point:
        """
        Updates the point position relative to its origin and notifies its users.
        """
        self.radius_delta = point.distance_from_origin(new_point)
        self.angle_delta = _atan2(new_point.y(), new_point.x())
        self._update_geometry()
        return self

    def set_absolute_point(self, new_point: static_point) -> point:
        """
        Updates the point absolute position and notifies its users.
        """
        delta_from_origin = new_point - self.origin.origin
        radius_target = point.distance(delta_from_origin, static_point(0., 0.))
        angle_target = _atan2(delta_from_origin.y(), delta_from_origin.x())
        self.radius_delta = radius_target - self.origin.radius
        self.angle_delta = angle_target - self.origin.angle
        self._update_geometry()
        return self


class selected_point(point):
    """
    A dynamic point with an position selected among a set of points with a selection function.
    """

    def __init__(self, points: _List[point], selector: _Callable) -> None:
        super().__init__(points[0])
        self._selector = selector
        self._points = []
        self.set_points(points)
        self._start_pos = static_point(self)

    def set_points(self, points: _List[point]) -> point:
        """
        Sets this point to be closest to a new set of points.
        """
        for pt in self._points:
            pt.remove_user(self)
        self._points = points
        for pt in self._points:
            pt.add_user(self)
        self._update_geometry()
        return self

    def _update_geometry(self) -> None:
        """
        Updates the point position when the set of points have moved.
        """
        new_pos = self._selector(self._points)
        if new_pos != self:
            super().set_absolute_point(new_pos)

