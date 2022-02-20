class color:
    """
    Color defined by its red, green blue and alpha values.
    Each value is between 0 and 255.
    TODO: use 0,1 range instead.
    """
    def __init__(self, r, g, b, a = 255):
        self.rgba = (r, g, b, a)

    @property
    def r(self):
        return self.rgba[0]

    @property
    def g(self):
        return self.rgba[1]

    @property
    def b(self):
        return self.rgba[2]

    @property
    def a(self):
        return self.rgba[3]

    def with_alpha(self, alpha):
        return color(self.r, self.g, self.b, alpha)

    def darker(self, percent):
        return self.adjust(10000. / percent)

    def lighter(self, percent):
        return self.adjust(percent)

    def adjust(self, percent):
        # TODO: convert to HSV and adjust V.
        rgba = list(self.rgba)
        for i in range(3):
            rgba[i] = max(0, min(255, int(self.rgba[i] * percent / 100.)))
        return color(*rgba)
