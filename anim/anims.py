from PyQt5.QtGui import QTransform
from .actor import actor
from .items import point
from . import trf

def reveal_item(animator, item, duration = 1.):
    if isinstance(item, actor):
        item = item.item
    animator.animate_value(0., 1., lambda opacity: item.setOpacity(opacity), None, duration)

def _rotate_around(point: point, center: point, angle: float):
    point.set_point(trf.rotate_around(point.original_point, center, angle))

def rotate_around(animator, point: point, center: point, start_angle: float, end_angle: float, duration =  1.):
    animator.animate_value(start_angle, end_angle, lambda angle: _rotate_around(point, center, angle), None, duration)

def rotate_item(animator, item, start_angle: float, end_angle:float , duration =  1.):
    if isinstance(item, actor):
        item = item.item
    animator.animate_value(item, start_angle, end_angle, lambda angle: item.setRotation(angle), None, duration)
