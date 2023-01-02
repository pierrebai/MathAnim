from .algorithms import find_all_of_type
from .items import item, point, static_point, rectangle, gray, no_color, static_rectangle
from .points import points
from .geometry import min_max

class geometries:
    """
    Containers of geometries for animations.

    Animations that you author can derive a geometries class from this to
    easily reset all opacities to zero and all geometries' points to their
    starting positions when the animation is reset.
    """
    def __init__(self, reset_opacities = True):
        self.reset_opacities = reset_opacities
        return super().__init__()

    def reset(self):
        for it in find_all_of_type(self.__dict__, item):
            it.reset()

    def create_background_rect(self, pts: points, min_margin = static_point(0.1, 0.1), max_margin = static_point(0.1, 0.1)):
        rect: static_rectangle = None
        for it in find_all_of_type(self.__dict__, item):
            it_rect: static_rectangle = it.scene_rect()
            if rect is None:
                rect = it_rect
            else:
                rect = rect.united(it_rect)
        min_pt, max_pt = rect.topLeft(), rect.bottomRight()
        delta = max_pt - min_pt
        delta = max(delta.x(), delta.y())
        p1 = point(min_pt - static_point(delta * min_margin.x(), delta * min_margin.y()))
        p2 = point(max_pt + static_point(delta * max_margin.x(), delta * max_margin.y()))
        return rectangle(p1, p2).outline(gray).thickness(5.).fill(no_color)

