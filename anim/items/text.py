from anim.items.rectangle import static_rectangle
from .point import point, relative_point, static_point
from .item import item

class scaling_text(item):
    """
    Text graphics item that follows the scene.
    """
    def __init__(self, label: str, pos: point, font_size: float = 10.) -> None:
        super().__init__(item.concrete.text(label))
        if isinstance(pos, relative_point):
            self._pos = relative_point(pos._origin, pos._start_pos)
        else:
            self._pos = relative_point(pos)
        self.set_serif_font(font_size)
        self._pos.add_user(self)
        self.update_geometry()

    def set_font(self, font_name, font_size):
        self.co_item.set_font(font_name, font_size)
        return self

    def set_serif_font(self, font_size: float = 10.):
        return self.set_font("Georgia", font_size)

    def set_sans_font(self, font_size: float = 10.):
        return self.set_font("Trebuchet MS", font_size)

    def get_font_size(self) -> float:
        return self.co_item.get_font_size()

    def get_font_name(self) -> str:
        return self.co_item.get_font_name()

    def center_on(self, other: item):
        self_rect = self.scene_rect()
        other_rect = other.scene_rect()
        self_center = self_rect.center
        other_center = other_rect.center
        delta = other_center - self_center
        self._pos.set_absolute_point(self._pos + delta)
        self.update_geometry()
        return self

    def place_above(self, pt: static_point):
        rect = self.scene_rect()
        bottom_center = static_point(rect.center.x, rect.center.y + rect.height / 2)
        delta = pt - bottom_center
        self._pos.set_absolute_point(self._pos + delta)
        self.update_geometry()
        return self

    def exponent_pos(self) -> relative_point:
        corner = self.scene_rect().top_right
        delta = corner - self._pos
        return relative_point(self._pos, delta)

    def scene_rect(self) -> static_rectangle:
        x1, y1, x2, y2 = self.co_item.scene_rect()
        return static_rectangle(static_point(x1, y1), static_point(x2, y2))


class fixed_size_text(scaling_text):
    """
    Text graphics item that ignores the scene transformation.
    """
    def __init__(self, text: str, pos: point, font_size: float = 10.) -> None:
        super().__init__(text, pos, font_size)
        self.co_item.set_fixed_size()
        self.update_geometry()
