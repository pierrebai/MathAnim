from PyQt5.QtGui import QTransform
from PyQt5.QtCore import QPointF

def rotate_around(pt: QPointF, center: QPointF, angle: float) -> QPointF:
    return QTransform().translate(center.x(), center.y()).rotate(angle).translate(-center.x(), -center.y()).map(pt)

def rotate_around_origin(pt: QPointF, angle: float) -> QPointF:
    return rotate_around(pt, QPointF(0., 0.), angle)
