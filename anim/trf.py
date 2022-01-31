from PySide6.QtGui import QTransform
from PySide6.QtCore import QPointF

from typing import List

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

def linear_serie(start: float, value: float, count: int) -> List[float]:
    """
    Create a list containing a geometric serie starting at a given value
    with successive values increasing by the value.
    """
    return [start + value * i for i in range(count)]

def geometric_serie(start: float, value: float, ratio: float, count: int) -> List[float]:
    """
    Create a list containing a geometric serie starting at a given value
    with successive values being in the given ratio.
    """
    return [start + value * (ratio ** i) for i in range(count)]

