from .item import item
from .color import color
from .colors import black
from .pen import pen
from .point import point, static_point
from .rectangle import static_rectangle

from typing import List as _List

from PySide6.QtWidgets import QGraphicsItemGroup as _Group


class group(_Group, item):
    """
    Item that can be animated.
    """
    def __init__(self, sub_items: _List[item] = None) -> None:
        self.sub_items = []
        super().__init__(None)
        self.set_items(sub_items)

    def reset(self):
        """
        Reset the item to its initial state.
        """
        for i in self.sub_items:
            i.reset()
        return super().reset()

    def set_items(self, sub_items: _List[item]) -> item:
        for i in self.sub_items:
            self.removeFromGroup(i)
        self.sub_items = sub_items or []
        for i in self.sub_items:
            self.addToGroup(i)

    def get_all_points(self) -> _List[point]:
        """
        Retrieve all animatable points in the item.
        """
        pts = []
        for i in self.sub_items:
            pts.extend(i.get_all_points())
        return pts

    def scene_rect(self) -> static_rectangle:
        if not self.sub_items:
            return static_rectangle()
        rect = None
        for i in self.sub_items:
            new_rect = i.scene_rect()
            if rect is None:
                rect = new_rect
            else:
                rect = rect.united(new_rect)
        return rect

    # Note: center_on will center all points. TODO: smarter center_on


    ########################################################################
    #
    # Colors

    def outline(self, new_color: color):
        """
        Sets the color of the pen used to draw the outline of the item.
        """
        for i in self.sub_items:
            i.outline(new_color)
        return self

    def get_outline(self) -> color:
        """
        Retrieves the outline color.
        """
        if self.sub_items:
            self.sub_items[0].get_outline()
        return black
        
    def thickness(self, new_width: float):
        """
        Sets the thickness of the pen used to draw the outline of the item.
        """
        for i in self.sub_items:
            i.thickness(new_width)
        return self

    def get_thickness(self) -> float:
        """
        Retrieves the thickness of the item outline.
        """
        if self.sub_items:
            self.sub_items[0].get_thickness()
        return 0.
        
    def fill(self, new_color: color):
        """
        Sets the color used to fill the item.
        """
        for i in self.sub_items:
            i.fill(new_color)
        return self

    def get_fill(self) -> color:
        """
        Retrieves the color used to fill the item.
        """
        if self.sub_items:
            self.sub_items[0].get_fill()
        return black


    ########################################################################
    #
    # Visibility

    def set_opacity(self, opacity):
        """
        Sets the opacity of the item, between 0 and 1.
        """
        for i in self.sub_items:
            i.set_opacity(opacity)
        return self

    def set_shown(self, shown: bool):
        """
        Shows or hides the item.
        """
        for i in self.sub_items:
            i.set_shown(shown)
        return self

    @property
    def shown(self) -> bool:
        """
        Verifies if the item is shown.
        """
        if self.sub_items:
            return self.sub_items[0].shown
        return False

    def set_z_order(self, order: float) -> item:
        """
        Set drawing priority, higher order is on top.
        """
        super().set_z_order(order)
        for i in self.sub_items:
            i.set_z_order(order)
        return self
