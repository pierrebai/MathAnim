from .types import find_all_of_type
from .items import point

class points:
    """
    Containers of points for animations.

    Animations that you author can derive a points class from this to
    easily reset all points to their starting positions when the
    animation is reset.
    """
    def __init__(self):
        return super().__init__()

    def reset(self):
        for pt in find_all_of_type(self.__dict__, point):
            pt.reset()
