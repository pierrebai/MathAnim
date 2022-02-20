from .items.point import static_point

from PySide6.QtGui import QTransform as _QTransform

def rotate_around(pt: static_point, center: static_point, angle: float) -> static_point:
    """
    Rotates a point around another point of the given angle in degrees.
    """
    return _QTransform().translate(center.x(), center.y()).rotate(angle).translate(-center.x(), -center.y()).map(pt)

def rotate_around_origin(pt: static_point, angle: float) -> static_point:
    """
    Rotates a point around the origin (0,0) of the given angle in degrees.
    """
    return rotate_around(pt, static_point(0., 0.), angle)

