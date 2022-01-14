from PyQt5.QtCore import QPointF

class point(QPointF):
    """
    A dynamic point that can be animated from its original position and which
    propagates its movement to dynamic graphics items built from it.
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
        self._start_pos = QPointF(x, y)
        self._users = []
        super().__init__(x, y)

    @property
    def original_point(self) -> QPointF:
        """
        The original position of the point, useful to animate from the starting position.
        """
        return self._start_pos

    def add_user(self, user) -> None:
        """
        Adds a user of the popint that will be notified when the point moves.
        """
        self._users.append(user)

    def remove_user(self, user) -> None:
        """
        Removes a user of the popint that was notified when the point moved.
        """
        self._users.remove(user)

    def set_point(self, new_point: QPointF) -> None:
        """
        Updates the point position and notifies its users.
        """
        if self != new_point:
            self.setX(new_point.x())
            self.setY(new_point.y())

            for u in self._users:
                u.update_geometry()


class relative_point(point):
    """
    A dynamic point with an position relative to another point, called its origin.
    """

    def __init__(self, origin: point, *args) -> None:
        super().__init__(*args)
        self._origin = origin
        self._delta = self._start_pos
        origin.add_user(self)
        self.update_geometry()

    def update_geometry(self):
        """
        Updates the point position relative to its origin when the point it is relative to has moved.
        """
        new_pos = self._origin + self._delta
        if new_pos != self:
            super().set_point(new_pos)

    def set_point(self, new_point: QPointF) -> None:
        """
        Updates the point position relative to its origin and notifies its users.
        """
        self._delta = new_point
        self.update_geometry()
