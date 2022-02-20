from .point import point, static_point
from .item import item

class static_rectangle:
    def __init__(self, p1: static_point, p2: static_point):
        self.p1 = p1
        self.p2 = p2

    @property
    def center(self) -> static_point:
        return (self.p1 + self.p2) / 2

    @property
    def width(self) -> float:
        return abs(self.p2.x - self.p1.x)

    @property
    def height(self) -> float:
        return abs(self.p2.y - self.p1.y)

    @property
    def top_right(self) -> static_point:
        return static_point(max(self.p2.x, self.p1.x), min(self.p2.y, self.p1.y))

    def scene_rect(self):
        return self

class rectangle(static_rectangle, item):
    """
    A rectangle graphics item that is dynamically updated when the two corner points move.
    """
    def __init__(self, p1: point, p2: point):
        static_rectangle.__init__(self, p1, p2)
        item.__init__(self, item.concrete.rectangle())
        p1.add_user(self)
        p2.add_user(self)
        self.update_geometry()

class center_rectangle(item):
    """
    A rectangle graphics item that is dynamically updated when its center point moves.
    """
    def __init__(self, center: point, half_width: float, half_height: float):
        super().__init__(item.concrete.rectangle())
        self.center = center
        self.corner_delta = static_point(half_width, half_height)
        center.add_user(self)
        self.update_geometry()

    @property
    def p1(self):
        return self.center - self.corner_delta

    @property
    def p2(self):
        return self.center + self.corner_delta

    def scene_rect(self) -> static_rectangle:
        return static_rectangle(self.p1, self.p2)

