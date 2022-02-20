from .color import color

class pen:
    """
    A pen used to draw outline in a given color and line width.
    """
    def __init__(self, co: color, width: float):
        self.color = co
        self.width = width
