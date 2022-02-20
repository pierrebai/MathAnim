class static_point:
    """
    A static point that does not propagate its position.
    Supports all kind of math operations: +, -, * etc.
    The additive operations take another point.
    The multiplicative operations take a floating-point value.
    """
    def __init__(self, *args):
        if len(args) == 0:
            x = 0
            y = 0
        elif len(args) == 1:
            x = args[0].x
            y = args[0].y
        else:
            x = args[0]
            y = args[1]
        self.x = x
        self.y = y

    def __neg__(self):
        return static_point(-self.x, -self.y)

    def __pos__(self):
        return static_point(self.x, self.y)

    def __abs__(self):
        return static_point(abs(self.x), abs(self.y))

    def __add__(self, pt):
        return static_point(self.x + pt.x, self.y + pt.y)

    def __sub__(self, pt):
        return static_point(self.x - pt.x, self.y - pt.y)
    
    def __mul__(self, val: float):
        return static_point(self.x * val, self.y * val)
    
    def __matmul__(self, val: float):
        return static_point(self.x @ val, self.y @ val)
    
    def __iadd__(self, pt):
        self.x += pt.x
        self.y += pt.y
        return self

    def __isub__(self, pt):
        self.x -= pt.x
        self.y -= pt.y
        return self
    
    def __imul__(self, val: float):
        self.x *= val
        self.y *= val
        return self
    
    def __imatmul__(self, val: float):
        self.x @= val
        self.y @= val
        return self
    
    def __rmul__(self, val: float):
        return static_point(self.x * val, self.y * val)
    
    def __rmatmul__(self, val: float):
        return static_point(self.x @ val, self.y @ val)
    
    def __truediv__(self, val: float):
        return static_point(self.x / val, self.y / val)
    
    def __floordiv__(self, val: float):
        return static_point(self.x // val, self.y // val)
    
    def __pow__(self, val: float):
        return static_point(self.x ** val, self.y ** val)
    
    
class point(static_point):
    """
    A dynamic point that can be animated from its original position and which
    propagates its movement to dynamic items built from it.
    """

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self._start_pos = static_point(self.x, self.y)
        self._users = []

    @property
    def original_point(self):
        """
        The original position of the point, useful to animate from the starting position.
        """
        return self._start_pos

    def add_user(self, user):
        """
        Adds a user of the popint that will be notified when the point moves.
        """
        self._users.append(user)
        return self

    def remove_user(self, user):
        """
        Removes a user of the popint that was notified when the point moved.
        """
        self._users.remove(user)
        return self

    def set_point(self, new_point: static_point):
        """
        Updates the point position and notifies its users.
        """
        if self != new_point:
            self.x, self.y = new_point.x, new_point.y

            for u in self._users:
                u.update_geometry()
        return self

    def set_absolute_point(self, new_point: static_point):
        """
        Updates the point absolute position and notifies its users.
        """
        self.set_point(new_point)
        return self

    def reset(self):
        """
        Resets the point to its original location.
        """
        self.set_point(self.original_point)
        return self


class relative_point(point):
    """
    A dynamic point with an position relative to another point, called its origin.
    """

    def __init__(self, origin: point, *args) -> None:
        super().__init__(*args)
        self._origin = None
        self._delta = static_point(self._start_pos)
        self.set_origin(origin)

    def set_origin(self, new_origin: point) -> point:
        """
        Sets the relative point to be relative to a new origin.
        """
        if self._origin:
            self._origin.remove_user(self)
        self._origin = new_origin
        new_origin.add_user(self)
        self.update_geometry()
        return self

    def update_geometry(self):
        """
        Updates the point position relative to its origin when the point it is relative to has moved.
        """
        new_pos = self._origin + self._delta
        if new_pos != self:
            super().set_point(new_pos)

    def set_point(self, new_point: static_point) -> point:
        """
        Updates the point position relative to its origin and notifies its users.
        """
        self._delta = static_point(new_point)
        self.update_geometry()
        return self

    def set_absolute_point(self, new_point: static_point) -> point:
        """
        Updates the point absolute position and notifies its users.
        """
        self._delta = new_point - self._origin
        self.update_geometry()
        return self

