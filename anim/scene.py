from .actor import actor
from .items import no_pen, create_pointing_arrow
from .point import point

from PySide6.QtGui import QPainter, QFont
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsItem, QGraphicsSimpleTextItem, QGraphicsRectItem
from PySide6.QtCore import Qt, QPointF, QMarginsF, QRectF, QPoint

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

        self.remove_all_items()
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

    def remove_all_items(self) -> None:
        self.scene.clear()

        self.title = QGraphicsSimpleTextItem()
        self.title.setFont(QFont("Georgia", 24))
        self.title.setFlag(QGraphicsSimpleTextItem.ItemIgnoresTransformations)
        self.scene.addItem(self.title)

        self.titleBox = QGraphicsRectItem(0, 0, 600, 20)
        self.titleBox.setPen(no_pen)
        self.scene.addItem(self.titleBox)

        self.description = QGraphicsSimpleTextItem()
        self.description.setFont(QFont("Georgia", 10))
        self.description.setFlag(QGraphicsSimpleTextItem.ItemIgnoresTransformations)
        self.scene.addItem(self.description)

        self.descriptionBox = QGraphicsRectItem(0, 0, 200, 600)
        self.descriptionBox.setPen(no_pen)
        self.scene.addItem(self.descriptionBox)

        arrow = create_pointing_arrow(point(0, 0), point(0, 0))
        self.pointing_arrow = actor("pointing arrow", "The arrow that points to what the description is talking about.", arrow)
        self.add_actor(self.pointing_arrow)

    def set_title(self, title: str) -> None:
        self.title.setText(title)
        self.ensure_all_contents_fit()

    def set_description(self, description: str) -> None:
        self.description.setText(description)
        self.ensure_all_contents_fit()

    def _get_actors_bounding_rect(self):
        self.scene.removeItem(self.title)
        self.scene.removeItem(self.titleBox)
        self.scene.removeItem(self.description)
        self.scene.removeItem(self.descriptionBox)
        self.scene.removeItem(self.pointing_arrow.item)
        # Note: we need to use itemsBoundingRect because sceneRect never shrink,
        #       so removing the title and description would have no effect.
        actors_rect = self.scene.itemsBoundingRect()
        self.scene.addItem(self.title)
        self.scene.addItem(self.titleBox)
        self.scene.addItem(self.description)
        self.scene.addItem(self.descriptionBox)
        self.scene.addItem(self.pointing_arrow.item)
        return actors_rect

    def _size_text_boxes(self):
        scaledRect = self.view.transform().map(QRectF(0., 0., 1., 1.)).boundingRect()
        scale = scaledRect.height()
        self.titleBox.setRect(QRectF(0, 0, 200 / scale, 40 / scale))
        lines = self.description.text().splitlines()
        lineCount = len(lines)
        letterCount = max([len(line) for line in lines]) if lines else 1
        self.descriptionBox.setRect(QRectF(0, 0, 6 * letterCount / scale, 24 * lineCount / scale))

    def _place_title_and_desc(self) -> None:
        self._size_text_boxes()
        actors_rect = self._get_actors_bounding_rect()

        viewTopLeft = self.view.mapFromScene(actors_rect.topLeft())
        topLeft = self.view.mapToScene(viewTopLeft - QPoint(0, self.title.font().pointSize() * 4))
        self.title.setPos(topLeft)
        self.titleBox.setPos(topLeft)

        viewTopRight = self.view.mapFromScene(actors_rect.topRight())
        topLeft = self.view.mapToScene(viewTopRight + QPoint(30, 0))
        self.description.setPos(topLeft)
        self.descriptionBox.setPos(topLeft)

    def ensure_all_contents_fit(self, margin: int = None) -> None:
        """
        If the scene contents does not fit the view then call adjust_view_to_fit()
        with the given margin or the default margin.
        """
        self._place_title_and_desc()

        viewRect = self.view.rect()
        viewTopLeft = viewRect.topLeft()
        viewBotRight = viewRect.bottomRight()

        sceneRect = self.scene.sceneRect()
        breathingRoom = QPoint(5, 5)
        sceneTopLeft = self.view.mapFromScene(sceneRect.topLeft()) - breathingRoom
        sceneBotRight = self.view.mapFromScene(sceneRect.bottomRight()) + breathingRoom

        dx1 = viewTopLeft.x() - sceneTopLeft.x()
        dy1 = viewTopLeft.y() - sceneTopLeft.y()

        dx2 = viewBotRight.x() - sceneBotRight.x()
        dy2 = viewBotRight.y() - sceneBotRight.y()

        if dx1 > 0 or dy1 > 0 or dx2 < 0 or dy2 < 0:
            self.adjust_view_to_fit(margin, False)


    def adjust_view_to_fit(self, margin: int = None, place_title_and_desc = True) -> None:
        """
        Fits the whole contents of the scene with the given margin
        or the default margin all around.
        """
        if place_title_and_desc:
            self._place_title_and_desc()

        if margin is None:
            margin = self.default_margin

        self.view.fitInView(self.scene.sceneRect().marginsAdded(QMarginsF(margin, margin, margin, margin)), Qt.KeepAspectRatio)
