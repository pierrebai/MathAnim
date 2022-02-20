from .items.point import static_point

from PySide6.QtGui import QTransform
from PySide6.QtCore import QPointF

def rotate_around(pt: static_point, center: static_point, angle: float) -> static_point:
    """
    Rotates a point around another point of the given angle in degrees.
    """
    rot_pt = QTransform().translate(center.x, center.y).rotate(angle).translate(-center.x, -center.y).map(QPointF(pt.x, pt.y))
    return static_point(rot_pt.x(), rot_pt.y())

def rotate_around_origin(pt: static_point, angle: float) -> static_point:
    """
    Rotates a point around the origin (0,0) of the given angle in degrees.
    """
    return rotate_around(pt, static_point(0., 0.), angle)

