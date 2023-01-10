from .actor import actor
from .view import view
from .items import create_pointing_arrow, point, item, static_point, static_rectangle, fixed_size_text

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
        self.view = view(margin)
        self.remove_all_items()

    def reset(self) -> None:
        """
        Resets to a new scene and resets the view.
        """
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

        self.main_title = fixed_size_text('', point(0., 0.), 36, True).set_sans_font(36, True)
        self.scene.addItem(self.main_title)
        self.subtitle = fixed_size_text('', point(0., 0.), 10)
        self.scene.addItem(self.subtitle)

        self.title = fixed_size_text('', point(0., 0.), 24, True).set_sans_font(24, True)
        self.scene.addItem(self.title)
        self.description = fixed_size_text('', point(0., 0.), 10)
        self.scene.addItem(self.description)

        arrow = create_pointing_arrow(point(0., 0.), point(0., 0.))
        self.pointing_arrow = actor("pointing arrow", "The arrow that points to what the description is talking about.", arrow)
        self.add_actor(self.pointing_arrow)


    ########################################################################
    #
    # Title and Description

    def set_main_title(self, title: str) -> None:
        """
        Sets the main title and redo its placement.
        """
        self.main_title.setText(title)
        self.view.preserve_transform()

    def set_subtitle(self, title: str) -> None:
        """
        Sets the subtitle and redo its placement.
        """
        self.subtitle.setText(title)
        self.view.preserve_transform()

    def set_shot_title(self, title: str) -> None:
        """
        Sets the shot title and redo its placement.
        """
        self.title.setText(title)
        self.view.preserve_transform()

    def set_shot_description(self, description: str) -> None:
        """
        Sets the shot description and redo its placement.
        """
        self.description.setText(description)
        self.view.preserve_transform()


    ########################################################################
    #
    # View Fitting

    def _get_items_rect(self) -> Tuple[static_rectangle, static_rectangle]:
        """
        Returns the boundary of non-title items and all items including title.
        """
        self.scene.removeItem(self.main_title)
        self.scene.removeItem(self.subtitle)
        self.scene.removeItem(self.title)
        self.scene.removeItem(self.description)
        self.scene.removeItem(self.pointing_arrow.item)
        # Note: we need to use itemsBoundingRect because sceneRect never shrink,
        #       so removing the title and description would have no effect.
        actors_rect = self.scene.itemsBoundingRect()

        self.scene.addItem(self.pointing_arrow.item)
        self.scene.addItem(self.main_title)
        self.scene.addItem(self.subtitle)
        self.scene.addItem(self.title)
        self.scene.addItem(self.description)
        scene_rect = self.scene.itemsBoundingRect()

        return actors_rect, scene_rect

    def _place_title_and_desc(self) -> static_rectangle:
        """
        Places the title above other items the description to their right.
        """
        actors_rect, scene_rect = self._get_items_rect()

        def text_height(t: fixed_size_text, factor: float) -> static_point:
            return t.boundingRect().height() * factor

        self.description.position.set_absolute_point(actors_rect.topRight() + static_point(30, 0))

        title_factor = 1.1 if self.title.text().strip() else 0.

        self.title.position.set_absolute_point(actors_rect.topLeft() - static_point(0, text_height(self.title, title_factor)))
        self.subtitle.position.set_absolute_point(self.title.position - static_point(-40, text_height(self.subtitle, 3.)))
        self.main_title.position.set_absolute_point(self.subtitle.position - static_point(60, text_height(self.main_title, 1.1)))

        return scene_rect

    def ensure_all_contents_fit(self) -> None:
        """
        Ensures the scene contents fit the view.
        """
        scene_rect = self._place_title_and_desc()
        self.view.fit_rectangle(scene_rect)

