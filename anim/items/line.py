from .point import point
from .item import item
from .rectangle import static_rectangle

class line(item):
    """
    A line item that is dynamically updated when the two end-points move.
    """
    def __init__(self, p1: point, p2: point):
        super().__init__(item.concrete.line())
        self.p1 = p1
        self.p2 = p2
        p1.add_user(self)
        p2.add_user(self)
        self.update_geometry()

    def scene_rect(self) -> static_rectangle:
        return static_rectangle(self.p1, self.p2)
