from .point import point

from PySide6.QtWidgets import QGraphicsSimpleTextItem
from PySide6.QtGui import QFont

class scaling_text(QGraphicsSimpleTextItem):
    """
    Text graphics item that follows the scene.
    """
    def __init__(self, text: str, pos: point, font_size: int = 10, parent = None) -> None:
        super().__init__(parent)
        self.pos = pos
        self.set_serif_font(font_size)
        pos.add_user(self)
        self.update_geometry()

    def set_serif_font(self, font_size: int = 10)-> None:
        self.setFont(QFont("Georgia", font_size))

    def set_sans_font(self, font_size: int = 10)-> None:
        self.setFont(QFont("Arial", font_size))

    def update_geometry(self):
        """
        Updates the text position after the point moved.
        """
        if self.pos != self.scenePos():
            self.prepareGeometryChange()
            self.setPos(self.pos)

class fixed_size_text(scaling_text):
    """
    Text graphics item that ignores the scene transformation.
    """
    def __init__(self, text: str, pos: point, font_size: int = 10, parent = None) -> None:
        super().__init__(text, pos, font_size, parent)
        self.setFlag(QGraphicsSimpleTextItem.ItemIgnoresTransformations)
