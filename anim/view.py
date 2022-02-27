from .items import static_point, static_rectangle

from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QGraphicsView
from PySide6.QtCore import Qt, QMarginsF, QRect, QPoint

from math import floor as _floor, ceil as _ceil


class view(QGraphicsView):
    """
    View of a scene, using Qt graphics view.

    The view can be zoomed and panned using the view transform.
    """

    def __init__(self, margin: int = 80) -> None:
        """
        Creates the scene (QGraphicsScene) and the view (QGraphicsView).
        Sets some useful default: anchored in teh center, no scrollbars,
        antialiasing and smooth pixmap transforms.
        """
        super().__init__(None)
        self.margin = margin
        self.zoom = 1.
        self._prev_delta = None

        self.setInteractive(False)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setOptimizationFlag(QGraphicsView.DontSavePainterState)

    def set_scene(self, scene):
        """
        Sets the scene used by the view.
        """
        self.setScene(scene.scene)
        return self

    def set_margin(self, margin):
        self.margin = margin
        return self


    ########################################################################
    #
    # View zoom and panning

    def set_zoom(self, zoom: float):
        self.zoom = zoom
        return self

    def fit_rectangle(self, rect: static_rectangle) -> None:
        """
        Fit the given rectangle to be visible in the view, with the current
        margins added around it.
        """
        margin = self.margin
        rect = rect.marginsAdded(QMarginsF(margin, margin, margin, margin))
        self.fitInView(rect, Qt.KeepAspectRatio)
        self.apply_transform(self.transform())

    def preserve_transform(self) -> None:
        """
        Preserve the current transaltion so it can be reapplied.
        """
        self._prev_delta = static_point(
            self.horizontalScrollBar().value(),
            self.verticalScrollBar().value())

    def apply_transform(self, trf) -> None:
        """
        Reapply the zoom and translation to the scene.
        """
        if trf:
            trf = trf.scale(self.zoom, self.zoom)
            self.setTransform(trf)
        if self._prev_delta and self.zoom > 1.:
            self.horizontalScrollBar().setValue(self._prev_delta.x())
            self.verticalScrollBar().setValue(self._prev_delta.y())


    ########################################################################
    #
    # Coordinate transforms

    def map_rect_to_scene(self, rect: static_rectangle) -> static_rectangle:
        # Unfortunately, Qt does *not* provide a mapToScene taking floating-point rect!
        return self.mapToScene(QRect(_floor(rect.x()), _floor(rect.y()), _ceil(rect.width()), _ceil(rect.height()))).boundingRect()

    def map_rect_from_scene(self, rect: static_rectangle) -> static_rectangle:
        return static_rectangle(self.mapfromScene(rect).boundingRect())

    def map_point_to_scene(self, pt: static_point) -> static_point:
        # Unfortunately, Qt does *not* provide a mapToScene taking floating-point point!
        return self.mapToScene(QPoint(round(pt.x()), round(pt.y())))

    def map_point_from_scene(self, pt: static_point) -> static_point:
        return static_point(self.mapFromScene(pt))

