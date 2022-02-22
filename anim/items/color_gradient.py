from .color import color
from ..types import find_all_of_type

from typing import List as _List
from math import floor as _floor

class color_gradient:
    def __init__(self, name: str, colors: _List[color], interpolate: bool = False) -> None:
        self.name = name
        self._colors = [color(c) for c in colors]
        self.interpolate = interpolate

    def reversed(self):
        new_gradient = color_gradient(self.name, self._colors, self.interpolate)
        new_gradient._colors.reverse()
        return new_gradient

    def interpolated(self, interpolate: bool):
        return color_gradient(self.name, self._colors, interpolate)

    def get_color(self, value, min_value, max_value):
        colors = self._colors
        if min_value >= max_value:
            return colors[0]
        if value <= min_value + 0.001:
            return colors[0]
        if value >= max_value - 0.001:
            return colors[-1]
        delta = max_value - min_value
        if self.interpolate and len(self._colors) > 1:
            index = _floor((value - min_value) * (len(colors) - 1) / delta)
            c1 = self._colors[index]
            c2 = self._colors[index+1]
            hsva = [(max(0., v1) + max(0., v2)) / 2 for v1, v2 in zip(c1.getHsvF(), c2.getHsvF())]
            return color.fromHsvF(*hsva)
        else:
            index = round((value - min_value) * (len(colors) - 1) / delta)
            return colors[index]


def from_colors(name: str, colors: _List[color], interpolate: bool = False) -> color_gradient:
    return color_gradient(name, colors)

def from_hexes(name: str, hexes: _List[int], interpolate: bool = True) -> color_gradient:
    return from_colors(name, [color(hex >> 16 & 0xFF, hex >> 8 & 0xFF, hex & 0xFF, 128) for hex in hexes])


def make_rainbow(count: int, alpha:float = 0.5) -> color_gradient:
    return color_gradient('Rainbow', [color.fromHsvF(float(i) / count, 1.0, 1.0, 0.5) for i in range(count)])

def make_grayscale(count: int, alpha:float = 0.5) -> color_gradient:
    return color_gradient('Grayscale', [color.fromHsvF(0., 0.0, 0.7 * i / count, 0.5) for i in range(count)])

rainbow = make_rainbow(64)
grayscale = make_grayscale(64)
black = color_gradient('Black', [color(0, 0, 0)])
#seaboard = from_hexes('Seaboard', [0x525564, 0x74828F, 0x96C0CE, 0xBEB9B5, 0xC25B56, 0xFEF6EB])
seaboard = from_hexes('Seaboard', [0x001219, 0x005f73, 0x0a9396, 0x94d2bd, 0xe9d8a6, 0xee9b00, 0xca6702, 0xbb3e03, 0xae2012, 0x9b2226])
sunrise  = from_hexes('Sunrise', [0x5aa9e6, 0x7fc8f8, 0xf9f9f9, 0xffe45e, 0xff6392])
primaries = from_hexes('Primary Colors', [0x1e91d6, 0x0072bb, 0x8fc93a, 0xe4cc37, 0xe18335])
powders = from_hexes('Powder', [0xfbf8cc, 0xfde4cf, 0xffcfd2, 0xf1c0e8, 0xcfbaf0, 0xa3c4f3, 0x90dbf4, 0x8eecf5, 0x98f5e1, 0xb9fbc0])
fire = from_hexes('Fire', [0x03071e, 0x370617, 0x6a040f, 0x9d0208, 0xd00000, 0xdc2f02, 0xe85d04, 0xf48c06, 0xfaa307, 0xffba08])

gradients = {
    gradient.name: gradient for gradient in find_all_of_type(globals(), color_gradient)
}
