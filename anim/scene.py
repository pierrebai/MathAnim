from .actor import actor
from .items import no_pen, create_pointing_arrow
from .point import point

from PySide6.QtGui import QPainter, QFont
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsItem, QGraphicsSimpleTextItem, QGraphicsRectItem
from PySide6.QtCore import Qt, QMarginsF, QRectF, QPoint, QRect

from typing import Tuple

class scene:
    """
    Scene containing scene items using Qt graphics scene and graphics items.
    """

    def __init__(self, margin: int = 80) -> None:
        """
        Creates the scene (QGraphicsScene) and the view (QGraphicsView).
        Sets some useful default: anchored in teh center, no scrollbars,
        antialiasing and smooth pixmap transforms.
        """
        super().__init__()
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

    def reset(self, margin: int = None) -> None:
        """
        Resets to a new scene and resets the view with the given margin
        or the default margin.
        """
        self.title = ""
        self.description = ""
        self.ensure_all_contents_fit(margin)
        
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
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)

        self.title = QGraphicsSimpleTextItem()
        self.title.setFont(QFont("Georgia", 24))
        self.title.setFlag(QGraphicsSimpleTextItem.ItemIgnoresTransformations)
        self.scene.addItem(self.title)

        self.title_box = QGraphicsRectItem(0, 0, 6, 2)
        self.title_box.setPen(no_pen)
        self.scene.addItem(self.title_box)

        self.description = QGraphicsSimpleTextItem()
        self.description.setFont(QFont("Georgia", 10))
        self.description.setFlag(QGraphicsSimpleTextItem.ItemIgnoresTransformations)
        self.scene.addItem(self.description)

        self.description_box = QGraphicsRectItem(0, 0, 2, 6)
        self.description_box.setPen(no_pen)
        self.scene.addItem(self.description_box)

        arrow = create_pointing_arrow(point(0, 0), point(0, 0))
        self.pointing_arrow = actor("pointing arrow", "The arrow that points to what the description is talking about.", arrow)
        self.add_actor(self.pointing_arrow)

    def set_title(self, title: str) -> None:
        self.title.setText(title)
        self.ensure_all_contents_fit()

    def set_description(self, description: str) -> None:
        self.description.setText(description)
        self.ensure_all_contents_fit()

    def _get_actors_rect(self) -> QRectF:
        self.scene.removeItem(self.title)
        self.scene.removeItem(self.title_box)
        self.scene.removeItem(self.description)
        self.scene.removeItem(self.description_box)
        self.scene.removeItem(self.pointing_arrow.item)
        # Note: we need to use itemsBoundingRect because sceneRect never shrink,
        #       so removing the title and description would have no effect.
        actors_rect = self.scene.itemsBoundingRect()
        self.scene.addItem(self.title_box)
        self.scene.addItem(self.description_box)
        self.scene.addItem(self.pointing_arrow.item)

        scene_rect = self.scene.itemsBoundingRect()

        self.scene.addItem(self.title)
        self.scene.addItem(self.description)
        
        return actors_rect, scene_rect

    def _size_text_boxes(self):
        letter_count = len(self.title.text())
        r = self.view.mapToScene(QRect(0, 0, 15 * letter_count, 40)).boundingRect()
        self.title_box.setRect(QRectF(0, 0, r.width(), r.height()))
        lines = self.description.text().splitlines()
        lineCount = len(lines)
        letter_count = max(36, max([len(line) for line in lines]) if lines else 1)
        r = self.view.mapToScene(QRect(0, 0, int(6.5 * letter_count), 20 * lineCount)).boundingRect()
        self.description_box.setRect(QRectF(0, 0, r.width(), r.height()))

    def _place_title_and_desc(self) -> QRectF:
        self._size_text_boxes()

        actors_rect, scene_rect = self._get_actors_rect()

        view_top_left = self.view.mapFromScene(actors_rect.topLeft())
        top_left = self.view.mapToScene(view_top_left - QPoint(0, self.title.font().pointSize() * 4))
        self.title.setPos(top_left)
        self.title_box.setPos(top_left)

        view_top_right = self.view.mapFromScene(actors_rect.topRight())
        top_left = self.view.mapToScene(view_top_right + QPoint(30, 0))
        self.description.setPos(top_left)
        self.description_box.setPos(top_left)

        return scene_rect

    def ensure_all_contents_fit(self, margin: int = None) -> None:
        """
        If the scene contents does not fit the view then call _adjust_view_to_fit()
        with the given margin or the default margin.
        """
        scene_rect = self._place_title_and_desc()
        margin = self.default_margin if margin is None else margin
        scene_rect = scene_rect.marginsAdded(QMarginsF(margin, margin, margin, margin))
        self._adjust_view_to_fit(scene_rect)

    def _adjust_view_to_fit(self, scene_rect: QRectF) -> None:
        """
        Fits the whole contents of the scene with the given margin
        or the default margin all around.
        """
        self.view.fitInView(scene_rect, Qt.KeepAspectRatio)
