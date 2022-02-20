from .color import color
from .pen import pen

from PySide6.QtGui import QBrush as _QBrush

class item:
    """
    Item that can be animated.
    """
    def __init__(self, _) -> None:
        pass
    
    def set_outline(self, new_pen: pen) -> None:
        """
        Sets the pen used to draw the outline of the item.
        """
        self.setPen(new_pen)
        
    def set_fill(self, new_color: color) -> None:
        """
        Sets the color used to fill the item.
        """
        self.setBrush(_QBrush(new_color))

    def set_opacity(self, opacity) -> None:
        """
        Sets the opacity of the item, between 0 and 1.
        """
        self.setOpacity(opacity)

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
