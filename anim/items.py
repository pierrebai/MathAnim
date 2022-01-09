from PyQt5.QtGui import QBrush, QColor, QPen, QPolygonF
from PyQt5.QtCore import QRectF, QPointF, QLineF
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsPolygonItem, QGraphicsLineItem, QGraphicsEllipseItem


"""
Helpers to create various kind of scene items.
"""

outer_size = 1000.
line_width = outer_size / 50.
dot_size = line_width * 1.5
tile_size = outer_size / 100.

no_color = QColor(0, 0, 0, 0)

orange_color    = QColor(235, 180,  40, 220)
blue_color      = QColor( 68, 125, 255, 200)
green_color     = QColor( 83, 223,  56, 200)
black_color     = QColor(  0,   0,   0)
cyan_color      = QColor( 30, 190, 220)
gray_color      = QColor(220, 220, 220, 120)
red_color       = QColor(255,  84,  46)

dark_orange_color   = orange_color.darker(130)
dark_blue_color     = blue_color.darker(130)
dark_green_color    = green_color.darker(130)
dark_cyan_color     = cyan_color.darker(130)
dark_gray_color     = gray_color.darker(130)
dark_red_color      = red_color.darker(130)

no_pen   = QPen(no_color, 0)
no_brush = QBrush(no_color)


cross_polygon = QPolygonF([
        QPointF(1, 3), QPointF(3, 1), QPointF(tile_size / 2, 3),
        QPointF(tile_size - 3, 1), QPointF(tile_size - 1, 3), QPointF(tile_size - 3, tile_size / 2),
        QPointF(tile_size - 1, tile_size - 3), QPointF(tile_size - 3, tile_size - 1), QPointF(tile_size / 2, tile_size - 3),
        QPointF(3, tile_size - 1), QPointF(1, tile_size - 3), QPointF(3, tile_size / 2),
])

arrow_polygon = QPolygonF([
    QPointF(2, 5), QPointF(tile_size / 2, 1), QPointF(tile_size - 2, 5),
    QPointF(tile_size / 2 + 1, 4), QPointF(tile_size / 2 + 1, tile_size - 1),
    QPointF(tile_size / 2 - 1, tile_size - 1), QPointF(tile_size / 2 - 1, 4), 
])

def create_cross(color: QColor = red_color):
    item = QGraphicsPolygonItem(cross_polygon)
    item.setBrush(QBrush(color))
    item.setPen(QPen(color.darker(130)))
    return item

def create_arrow(rotation_angle, color: QColor = black_color):
    item = QGraphicsPolygonItem(arrow_polygon)
    item.setPen(no_pen)
    item.setTransformOriginPoint(tile_size / 2, tile_size / 2)
    item.setRotation(rotation_angle)
    item.setBrush(QBrush(color))
    return item

def create_circle(radius, color: QColor = dark_blue_color, thickness = line_width):
    item = QGraphicsEllipseItem(-radius, -radius, radius * 2, radius * 2)
    item.setPen(QPen(color, thickness))
    item.setBrush(no_brush)
    item.setTransformOriginPoint(0, 0)
    return item

def create_disk(radius = dot_size, color: QColor = gray_color):
    item = QGraphicsEllipseItem(-radius, -radius, radius * 2, radius * 2)
    item.setPen(QPen(no_color, 0))
    item.setBrush(color)
    item.setTransformOriginPoint(0, 0)
    return item

def create_line(line: QLineF, color: QColor = green_color, thickness = line_width):
    item = QGraphicsLineItem(line)
    item.setPen(QPen(color, thickness))
    item.setTransformOriginPoint(line.p1())
    return item

def create_polygon(pts, color: QColor = dark_gray_color, thickness = line_width):
    item = QGraphicsPolygonItem(QPolygonF(pts))
    item.setPen(QPen(color, thickness))
    item.setBrush(no_color)
    return item
