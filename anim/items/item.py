import anim_qt

class item:
    """
    Item that can be animated.
    Uses a concrete_item internally to do the rendering.
    """
    concrete = anim_qt.items

    def __init__(self, co_item):
        self.co_item = co_item
    
    def update_geometry(self):
        """
        Updates the geometry of the concrete item by passing itself to it.
        """
        if self.co_item:
            self.co_item.update_geometry(self)

    def set_outline(self, pen):
        """
        Sets the pen used to draw the outline of the item.
        """
        if self.co_item:
            self.co_item.set_outline(pen)
        
    def set_fill(self, color):
        """
        Sets the color used to fill the item.
        """
        if self.co_item:
            self.co_item.set_fill(color)

    def set_opacity(self, opacity):
        """
        Sets the opacity of the item, between 0 and 1.
        """
        if self.co_item:
            self.co_item.set_opacity(opacity)

    def show(self, shown: bool) -> None:
        """
        Shows or hides the item.
        """
        if self.co_item:
            self.co_item.set_shown(shown)

    @property
    def shown(self) -> bool:
        """
        Verifies if the item is shown.
        """
        return self.co_item and self.co_item.get_shown()

    def reset(self) -> None:
        """
        Resets the item, get rid of the concrete item.
        """
        self.co_item = None

