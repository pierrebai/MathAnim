from .concrete_item_qt import concrete_item_qt

from PySide6.QtWidgets import QGraphicsSimpleTextItem
from PySide6.QtGui import QFont
from PySide6.QtCore import QPointF

class text(QGraphicsSimpleTextItem, concrete_item_qt):
    """
    Text graphics item that follows the scene.
    """
    def __init__(self, label: str, parent = None) -> None:
        super().__init__(label, parent)

    def set_font(self, font_name, font_size) -> QGraphicsSimpleTextItem:
        font = QFont(font_name)
        font.setPointSizeF(max(0.5, font_size))
        self.setFont(font)
        return self

    def get_font_size(self) -> float:
        return self.font().pointSizeF()

    def get_font_name(self) -> str:
        return self.font().name()

    def set_fixed_size(self):
        self.setFlag(QGraphicsSimpleTextItem.ItemIgnoresTransformations)

    def update_geometry(self, new_text):
        """
        Updates the text position after the point moved.
        """
        new_pos = QPointF(new_text._pos.x, new_text._pos.y)
        if new_pos != self.scenePos():
            self.prepareGeometryChange()
            self.setPos(new_pos)

    def scene_rect(self):
        rect = self.sceneBoundingRect()
        tl = rect.topLeft()
        br = rect.bottomRight()
        return (tl.x(), tl.y(), br.x(), br.y())
