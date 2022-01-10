from PyQt5.QtGui import QTransform
from PyQt5.QtWidgets import QGraphicsItem
from .actor import actor

from math import radians

def reveal_with_opacity(animator, item, duration_fraction = 1.):
    if isinstance(item, actor):
        item = item.item
    animator.add_anim_value(item, 0., 1., lambda opacity: item.setOpacity(opacity), None, duration_fraction)

def _rotate_around(item: QGraphicsItem, angle, rot_x, rot_y):
    item.setTransform(QTransform().translate(-rot_x, -rot_y).rotate(angle).translate(rot_x, rot_y), False)

def rotate_around(animator, item: QGraphicsItem, start_angle, end_angle, rot_x, rot_y, duration_fraction =  1.):
    if isinstance(item, actor):
        item = item.item
    pos = item.pos()
    item_rot_x = pos.x() - rot_x
    item_rot_y = pos.y() - rot_y
    animator.add_anim_value(item, start_angle, end_angle, lambda angle: _rotate_around(item, angle, item_rot_x, item_rot_y), None, duration_fraction)

def rotate(animator, item: QGraphicsItem, start_angle, end_angle, duration_fraction =  1.):
    if isinstance(item, actor):
        item = item.item
    animator.add_anim_value(item, start_angle, end_angle, lambda angle: item.setRotation(angle), None, duration_fraction)
