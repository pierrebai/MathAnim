from .trf import pi, hpi, tau
from .algorithms import deep_map

from math import sin, exp, log
from typing import List as _List, Callable as _Callable, Any as _Any
from collections import namedtuple as _namedtuple

#################################################################
#
# Float animations

def linear_serie(start: int|float, value: int|float, count: int) -> _List[int|float]:
    """
    Create a list containing a geometric serie starting at a given value
    with successive values increasing by the value.
    """
    return [start + value * i for i in range(count)]

def geometric_serie(start: int|float, value: int|float, ratio: int|float, count: int) -> _List[int|float]:
    """
    Create a list containing a geometric serie starting at a given value
    with successive values being in the given ratio.
    """
    return [start + value * (ratio ** i) for i in range(count)]

def scaled_serie(value: float, count: int, scaler: _Callable) -> _List[float]:
    """
    Create a list containing a serie based on the given value and
    the scaler. The scaler should take a value between 0 and 1 as
    input and produce a factor to multiply the value.
    """
    fc = float(count - 1)
    return [value * scaler(i / fc) for i in range(count)]

def ondulation_serie(value: float, factor: float, count: int) -> _List[float]:
    """
    Create an ondulating series that goes from value / factor to value * factor.
    """
    log_factor = log(factor)
    def scaler(fraction: float) -> float:
        return exp(log_factor * sin(tau * fraction))
    return scaled_serie(value, count, scaler)


#################################################################
#
# Spread of things.

class spread_item:
    def __init__(self, row, col, index):
        self.row = row
        self.column = col
        self.index = index

def create_spread(counts: _List[int]) -> _List[_List[spread_item]]:
    """
    Given a list of counts, create a spread (list of of lists) of that many spread item.
    The spread item conyain the row, column and overall index of the item in the spread.
    """
    spread = []
    index = 0
    for row, count in enumerate(counts):
        spread.append([spread_item(row, column, index + column) for column in range(count)])
        index += count
    return spread

def create_triangle_spread(rows: int) -> _List[_List[spread_item]]:
    """
    Given a number of rows, create a triangular spread.
    """
    return create_spread(linear_serie(1, 1, rows))

def create_triangle_odd_spread(rows: int) -> _List[_List[spread_item]]:
    """
    Given a number of rows, create a triangular spread.
    """
    return create_spread(linear_serie(1, 2, rows))

def create_rectangle_spread(width: int, height: int) -> _List[_List[spread_item]]:
    """
    Given a width and height, create a rectangular spread.
    """
    return create_spread([width] * height)

def create_square_spread(rows: int) -> _List[_List[spread_item]]:
    """
    Given a number of rows, create a square spread.
    """
    return create_spread([rows] * rows)

