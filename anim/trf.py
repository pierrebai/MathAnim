from PySide6.QtGui import QTransform
from PySide6.QtCore import QPointF

def rotate_around(pt: QPointF, center: QPointF, angle: float) -> QPointF:
    """
    Rotates a point around another point of the given angle in degrees.
    """
    return QTransform().translate(center.x(), center.y()).rotate(angle).translate(-center.x(), -center.y()).map(pt)

def rotate_around_origin(pt: QPointF, angle: float) -> QPointF:
    """
    Rotates a point around the origin (0,0) of the given angle in degrees.
    """
    return rotate_around(pt, QPointF(0., 0.), angle)
