from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtCore import QMarginsF, QRectF, Qt


class scene:
    """
    Scene containing scene items using Qt graphics scene and graphics items.
    """

    def __init__(self, margin = 10):
        """
        Creates the scene (QGraphicsScene) and the view (QGraphicsView).
        Sets some useful default: anchored in teh center, no scrollbars,
        antialiasing and smooth pixmap transforms.
        """
        self.default_margin = margin
        self.view = QGraphicsView()
        self.view.setInteractive(False)
        self.view.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.reset()

    def get_widget(self):
        """
        Retrieves the view (QGraphicsView).
        """
        return self.view

    def add_item(self, item):
        self.scene.addItem(item)

    def reset(self, margin = None):
        """
        Resets to a new scene and resets the view with the given margin
        or the default margin.
        """
        self.scene = QGraphicsScene()

        self.view.setScene(self.scene)
        self.view.resetTransform()
        self.view.resetCachedContent()
        self.view.setSceneRect(QRectF())

        self.adjust_view_to_fit(margin)
        
    def ensure_all_contents_fit(self, margin = None):
        """
        If the scene contents does not fit the view then call adjust_view_to_fit()
        with the given margin or the default margin.
        """
        viewOrigin = self.view.rect().topLeft()
        sceneOrigin = self.view.mapFromScene(self.scene.sceneRect().translated(-15, -15).topLeft())
        if viewOrigin.x() >= sceneOrigin.x() or viewOrigin.y() >= sceneOrigin.y():
            self.adjust_view_to_fit(margin)

    def adjust_view_to_fit(self, margin = None):
        """
        Fits the whole contents of the scene with the given margin
        or the default margin all around.
        """
        if margin is None:
            margin = self.default_margin
        self.view.fitInView(self.scene.sceneRect().marginsAdded(QMarginsF(margin, margin, margin, margin)), Qt.KeepAspectRatio)
