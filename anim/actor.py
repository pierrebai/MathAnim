from .named import named
from .items import item

from PySide6.QtWidgets import QGraphicsItem

class actor(named):
    """
    A named actor used in an animation.
    The actor contains a named item. This is what gets animated.
    """

    def __init__(self, name: str, description: str, item: item) -> None:
        super(actor, self).__init__(name, description)
        self.item = item
        self.reset()

    def reset(self) -> None:
        """
        Resets the actor. Make it shown.
        """
        self.show(True)

    def show(self, shown: bool) -> None:
        """
        Shows or hides the actor's item.
        """
        self.item.set_shown(shown)

    @property
    def shown(self) -> bool:
        """
        Verifies if the actor is shown.
        """
        return self.item.shown

