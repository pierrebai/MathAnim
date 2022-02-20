from .point import point, relative_point, static_point
from .item import item
from .rectangle import static_rectangle

from typing import List

class polygon(item):
    """
    A polygon graphics item that is dynamically updated when its points move.
    """
    def __init__(self, points: List[point]):
        super().__init__(item.concrete.polygon())
        self.points = points
        for pt in points:
            pt.add_user(self)
        self.update_geometry()

    def center(self) -> relative_point:
        if not self.points:
            return relative_point(point(0., 0))
        center = static_point(0., 0.)
        for pt in self.points:
            center += pt
        center = center / float(len(self.points))
        delta = center - self.points[0]
        return relative_point(self.points[0], delta)

    def top_left(self) -> relative_point:
        if not self.points:
            return relative_point(point(0., 0))
        min_x = 1000000
        min_y = 1000000
        for pt in self.points:
            min_x = min(pt.x(), min_x)
            min_y = min(pt.y(), min_y)
        corner = QPointF(min_x, min_y)
        delta = corner - self.points[0]
        return relative_point(self.points[0], delta)

    def scene_rect(self) -> static_rectangle:
        if not self.points:
            return static_rectangle(static_point(0., 0), static_point(0., 0))
        p1 = static_point(self.points[0])
        p2 = static_point(self.points[0])
        for pt in self.points:
            p1.x = min(pt.x, p1.x)
            p1.y = min(pt.y, p1.y)
            p2.x = max(pt.x, p2.x)
            p2.y = max(pt.y, p2.y)
        return static_rectangle(p1, p2)
