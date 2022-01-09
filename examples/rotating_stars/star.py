class star:
    """
    Describes a rotating stars.
    """
    def __init__(self, sides: int = 7, skip: int = 3, ratio = 0.9):
        self.sides = sides
        self.skip = skip
        self.inner_circle_ratio = float(skip) / float(sides)
        self.inner_circle_dot_ratio = ratio

class star_options:
    """
    Options when drawing the rotating stars.
    """

    def __init__(self):
        self.draw_intra_circle_polygons = True
        self.draw_inter_circle_polygons = True
        self.draw_dots = True
        self.draw_inner_circles = True
        self.draw_outer_circle = True
        self.draw_star = True
