from .actor import actor
from .view import view
from .items import create_pointing_arrow, point, item, static_point, static_rectangle

from PySide6.QtGui import QFont, QPen, QColor
from PySide6.QtWidgets import QGraphicsScene, QGraphicsSimpleTextItem, QGraphicsRectItem

from typing import Tuple

class scene:
    """
    Scene containing scene items using Qt graphics scene, view and graphics items.

    The scene can show a title and description in the scene. It positions the title
    above all other items. It position the description on the right of all items.

    The scene also has a pointing arrow. It is used to point from the description
    to what is described.

    The scene tries to show all its item in the scene view by manipulating the
    view transform.
    """

    def __init__(self, margin: int = 80) -> None:
        """
        Creates the scene (QGraphicsScene) and the view.
        """
        super().__init__()
        self.view = view()
        self.remove_all_items()

    def reset(self, margin: int = None) -> None:
        """
        Resets to a new scene and resets the view with the given margin
        or the default margin.
        """
        self.title = ""
        self.description = ""
        self.view.preserve_transform()
        self.ensure_all_contents_fit()
        
    def get_widget(self) -> view:
        """
        Retrieves the view.
        """
        return self.view


    ########################################################################
    #
    # Actors

    def add_item(self, item: item) -> None:
        self.scene.addItem(item)

    def add_actor(self, actor: actor) -> None:
        self.add_item(actor.item)

    def remove_item(self, item: item) -> None:
        if item.scene() == self.scene:
            self.scene.removeItem(item)

    def remove_actor(self, actor: actor) -> None:
        self.remove_item(actor.item)

    def remove_all_items(self) -> None:
        """
        Removes all items from the scene.
        """
        self.scene = QGraphicsScene()
        self.scene.setItemIndexMethod(QGraphicsScene.ItemIndexMethod.NoIndex)
        self.view.set_scene(self)

        self.title = QGraphicsSimpleTextItem()
        self.title.setFont(QFont("Georgia", 24))
        self.title.setFlag(QGraphicsSimpleTextItem.ItemIgnoresTransformations)
        self.scene.addItem(self.title)

        self.title_box = QGraphicsRectItem(0, 0, 6, 2)
        self.title_box.setPen(QPen(QColor(0, 0, 0, 0), 0))
        self.scene.addItem(self.title_box)

        self.description = QGraphicsSimpleTextItem()
        self.description.setFont(QFont("Georgia", 10))
        self.description.setFlag(QGraphicsSimpleTextItem.ItemIgnoresTransformations)
        self.scene.addItem(self.description)

        self.description_box = QGraphicsRectItem(0, 0, 2, 6)
        self.description_box.setPen(QPen(QColor(0, 0, 0, 0), 0))
        self.scene.addItem(self.description_box)

        arrow = create_pointing_arrow(point(0., 0.), point(0., 0.))
        self.pointing_arrow = actor("pointing arrow", "The arrow that points to what the description is talking about.", arrow)
        self.add_actor(self.pointing_arrow)


    ########################################################################
    #
    # Title and Description

    def set_title(self, title: str) -> None:
        """
        Sets the title and redo its placement.
        """
        self.title.setText(title)
        self.view.preserve_transform()
        self.ensure_all_contents_fit()

    def set_description(self, description: str) -> None:
        """
        Sets the description and redo its placement.
        """
        self.description.setText(description)
        self.view.preserve_transform()
        self.ensure_all_contents_fit()


    ########################################################################
    #
    # View Fitting

    def _get_items_rect(self) -> Tuple[static_rectangle, static_rectangle]:
        """
        Returns the boundary of non-title items and all items including title.
        """
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
        """
        Because the title and desciption are not transformed, the scene
        does not calculate their size and boundaries correctly.
        We use invisible boxes to fix that.
        """
        letter_count = len(self.title.text())
        r = self.view.map_rect_to_scene(static_rectangle(0, 0, 15 * letter_count, 40))
        self.title_box.setRect(static_rectangle(0, 0, r.width(), r.height()))
        lines = self.description.text().splitlines()
        lineCount = len(lines)
        letter_count = max(36, max([len(line) for line in lines]) if lines else 1)
        r = self.view.map_rect_to_scene(static_rectangle(0, 0, int(6.5 * letter_count), 20 * lineCount))
        self.description_box.setRect(static_rectangle(0, 0, r.width(), r.height()))

    def _place_title_and_desc(self) -> static_rectangle:
        """
        Places the title above other items the description to their right.
        """
        self._size_text_boxes()

        actors_rect, scene_rect = self._get_items_rect()

        view_top_left = self.view.map_point_from_scene(actors_rect.topLeft())
        top_left = self.view.map_point_to_scene(view_top_left - static_point(0, self.title.font().pointSize() * 1.5))
        self.title.setPos(top_left)
        self.title_box.setPos(top_left)

        view_top_right = self.view.map_point_from_scene(actors_rect.topRight())
        top_left = self.view.map_point_to_scene(view_top_right + static_point(30, 0))
        self.description.setPos(top_left)
        self.description_box.setPos(top_left)

        return scene_rect

    def ensure_all_contents_fit(self) -> None:
        """
        Ensures the scene contents fit the view.
        """
        scene_rect = self._place_title_and_desc()
        self.view.fit_rectangle(scene_rect)

