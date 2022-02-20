from .point import point
from .item import item
from .rectangle import static_rectangle


class pointing_arrow(item):
    """
    A curvy pointing arrow graphics item that is dynamically updated when the head or tail move.
    """
    def __init__(self, tail: point, head: point) -> None:
        super().__init__(item.concrete.pointing_arrow())
        self.head = None
        self.tail = tail
        tail.add_user(self)
        self.set_head(head)

    def set_head(self, new_head):
        """
        Sets a new point to be the head.
        """
        if self.head:
            self.head.remove_user(self)
        self.head = new_head
        new_head.add_user(self)
        self.update_geometry()
        return self

    def set_tail(self, new_tail):
        """
        Sets a new point to be the tail.
        """
        if self.tail:
            self.tail.remove_user(self)
        self.tail = new_tail
        new_tail.add_user(self)
        self.update_geometry()
        return self

    def scene_rect(self) -> static_rectangle:
        return static_rectangle(self.head, self.tail)

