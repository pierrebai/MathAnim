from .actor import actor

from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsItem
from PySide6.QtCore import QMarginsF, QRectF, Qt

class scene:
    """
    Scene containing scene items using Qt graphics scene and graphics items.
    """

    def __init__(self, margin: int = 10) -> None:
        """
        Creates the scene (QGraphicsScene) and the view (QGraphicsView).
        Sets some useful default: anchored in teh center, no scrollbars,
        antialiasing and smooth pixmap transforms.
        """
        self.default_margin = margin

        self.scene = QGraphicsScene()
        self.scene.setItemIndexMethod(QGraphicsScene.ItemIndexMethod.NoIndex)

        self.view = QGraphicsView()
        self.view.setInteractive(False)
        self.view.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.view.setScene(self.scene)

        self.adjust_view_to_fit(margin)

    def reset(self, margin: int = None) -> None:
        """
        Resets to a new scene and resets the view with the given margin
        or the default margin.
        """
        pass
        
    def get_widget(self) -> QGraphicsView:
        """
        Retrieves the view (QGraphicsView).
        """
        return self.view

    def add_item(self, item: QGraphicsItem) -> None:
        self.scene.addItem(item)

    def add_actor(self, actor: actor) -> None:
        self.add_item(actor.item)

    def remove_item(self, item: QGraphicsItem) -> None:
        if item.scene() == self.scene:
            self.scene.removeItem(item)

    def remove_actor(self, actor: actor) -> None:
        self.remove_item(actor.item)

    def ensure_all_contents_fit(self, margin: int = None) -> None:
        """
        If the scene contents does not fit the view then call adjust_view_to_fit()
        with the given margin or the default margin.
        """
        viewOrigin = self.view.rect().topLeft()
        sceneOrigin = self.view.mapFromScene(self.scene.sceneRect().translated(-15, -15).topLeft())
        if viewOrigin.x() >= sceneOrigin.x() or viewOrigin.y() >= sceneOrigin.y():
            self.adjust_view_to_fit(margin)

    def adjust_view_to_fit(self, margin: int = None) -> None:
        """
        Fits the whole contents of the scene with the given margin
        or the default margin all around.
        """
        if margin is None:
            margin = self.default_margin
        self.view.fitInView(self.scene.sceneRect().marginsAdded(QMarginsF(margin, margin, margin, margin)), Qt.KeepAspectRatio)
