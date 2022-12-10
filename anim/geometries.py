from .types import find_all_of_type
from .items import item, circle

class geometries:
    """
    Containers of geometries for animations.

    Animations that you author can derive a geometries class from this to
    easily reset all opacities to zero and all geometries' points to their
    starting positions when the animation is reset.
    """
    def __init__(self):
        return super().__init__()

    def reset(self):
        for it in find_all_of_type(self.__dict__, item):
            it.set_opacity(0.)
            for pt in it.get_all_points():
                pt.reset()
