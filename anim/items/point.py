from PySide6.QtCore import QPointF as _QPointF
from typing import List as _List, Callable as _Callable

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
        self.set_point(self.original_point)
        return self

    def distance_squared(self, pt: static_point) -> float:
        delta = self - pt
        return delta.x() ** 2 + delta.y() ** 2



class relative_point(point):
    """
    A dynamic point with an position relative to another point, called its origin.
    """

    def __init__(self, origin: point, *args) -> None:
        super().__init__(*args)
        self._origin = None
        self.delta = static_point(self._start_pos)
        self.set_origin(origin)

    def set_delta(self, new_delta: static_point) -> point:
        if self.delta != new_delta:
            self.delta = new_delta
            self._update_geometry()
        return self

    def set_origin(self, new_origin: point) -> point:
        """
        Sets this relative point to be relative to a new origin.
        """
        if self._origin:
            self._origin.remove_user(self)
        self._origin = new_origin
        new_origin.add_user(self)
        self._update_geometry()
        return self

    def _update_geometry(self) -> None:
        """
        Updates the point position relative to its origin when the point it is relative to has moved.
        """
        new_pos = self._origin + self.delta
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
        self.delta = new_point - self._origin
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
            super().set_point(new_pos)

