from anim.items.concrete_item import concrete_item

from PySide6.QtGui import QPen, QBrush, QColor


class concrete_item_qt(concrete_item):
    
    def set_outline(self, pen) -> None:
        self.setPen(QPen(QColor(pen.color.r, pen.color.g, pen.color.b, pen.color.a), pen.width))
        
    def set_fill(self, color) -> None:
        self.setBrush(QBrush(QColor(color.r, color.g, color.b, color.a)))

    def set_opacity(self, opacity) -> None:
        self.setOpacity(opacity)

    def set_shown(self, shown: bool) -> None:
        self.setVisible(shown)

    def get_shown(self) -> bool:
        return self.isVisible()

