from .color import color
from .pen import pen
from .point import point

from PySide6.QtGui import QBrush as _QBrush

from typing import List as _List

class item:
    """
    Item that can be animated.
    """
    def __init__(self, _) -> None:
        pass


    ########################################################################
    #
    # Points

    def get_all_points(self) -> _List[point]:
        """
        Retrieve all animatable points in the item.
        """
        return []


    ########################################################################
    #
    # Colors

    def outline(self, new_color: color):
        """
        Sets the color of the pen used to draw the outline of the item.
        """
        self.setPen(pen(new_color, self.pen().widthF()))
        return self
        
    def thickness(self, new_width: float):
        """
        Sets the thickness of the pen used to draw the outline of the item.
        """
        self.setPen(pen(self.pen().color(), new_width))
        return self
        
    def fill(self, new_color: color):
        """
        Sets the color used to fill the item.
        """
        self.setBrush(_QBrush(new_color))
        return self


    ########################################################################
    #
    # Visibility

    def set_opacity(self, opacity):
        """
        Sets the opacity of the item, between 0 and 1.
        """
        self.setOpacity(opacity)
        return self

    def set_shown(self, shown: bool) -> None:
        """
        Shows or hides the item.
        """
        self.setVisible(shown)

    @property
    def shown(self) -> bool:
        """
        Verifies if the item is shown.
        """
        return self.isVisible()
