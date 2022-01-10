from .named import named

from PyQt5.QtWidgets import QGraphicsItem

class actor(named):
    """
    A named actor item used in an animation.
    By default the actor is invisible in the scene.
    """

    def __init__(self, name: str, description: str, item: QGraphicsItem) -> None:
        super(actor, self).__init__(name, description)
        self.item = item
        self.reset()

    def reset(self) -> None:
        self.show(True)

    def show(self, shown: bool) -> None:
        self.item.setVisible(shown)

    @property
    def shown(self) -> bool:
        return self.item.isVisible()

