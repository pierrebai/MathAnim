from .color import color
from .pen import pen
from .point import point, static_point

from PySide6.QtGui import QBrush as _QBrush

from typing import List as _List

class item:
    """
    Item that can be animated.
    """
    def __init__(self, _) -> None:
        pass

    def reset(self):
        """
        Reset the item to its initial state.
        """
        self.set_opacity(0.)
        for pt in self.get_all_points():
            pt.reset()
        return self


    ########################################################################
    #
    # Points

    def get_all_points(self) -> _List[point]:
        """
        Retrieve all animatable points in the item.
        """
        return []

    def scene_rect(self):
        pass

    def center_on(self, other):
        """
        Centers this item on the given item.
        """
        self_center  = self.scene_rect().center()
        other_center = other if isinstance(other, static_point) else other.scene_rect().center()
        delta = other_center - self_center
        for pt in self.get_all_points():
            pt.set_absolute_point(pt + delta)
        return self


    ########################################################################
    #
    # Colors

    def outline(self, new_color: color):
        """
        Sets the color of the pen used to draw the outline of the item.
        """
        self.setPen(pen(new_color, self.pen().widthF()))
        return self

    def get_outline(self) -> color:
        """
        Retrieves the outline color.
        """
        return self.pen().color()
        
    def thickness(self, new_width: float):
        """
        Sets the thickness of the pen used to draw the outline of the item.
        """
        self.setPen(pen(self.pen().color(), new_width))
        return self

    def get_thickness(self) -> float:
        """
        Retrieves the thickness of the item outline.
        """
        return self.pen().widthF()
        
    def fill(self, new_color: color):
        """
        Sets the color used to fill the item.
        """
        self.setBrush(_QBrush(new_color))
        return self

    def get_fill(self) -> color:
        """
        Retrieves the color used to fill the item.
        """
        return self.brush().color()


    ########################################################################
    #
    # Visibility

    def set_opacity(self, opacity):
        """
        Sets the opacity of the item, between 0 and 1.
        """
        self.setOpacity(opacity)
        return self

    def set_shown(self, shown: bool):
        """
        Shows or hides the item.
        """
        self.setVisible(shown)
        return self

    @property
    def shown(self) -> bool:
        """
        Verifies if the item is shown.
        """
        return self.isVisible()

    def set_z_order(self, order: float):
        """
        Set drawing priority, higher order is on top.
        """
        self.setZValue(order)
        return self