class Circle:
    """Circle is a circle on screen (fruit or movable)"""

    def __init__(self, radius, xy, color):
        self.xy = xy
        self.color = color
        self.radius = radius

    def set_pos(self, pos):
        self.xy = pos

    def set_radius(self, radius):
        self.radius = radius

    def set_color(self, color):
        self.color = color

    def get_pos(self):
        return self.xy

    def get_color(self):
        return self.color

    def get_radius(self):
        return self.radius

    def circle_center_inside_self(self, circle):
        """Return if circle is inside of self"""
        return (self.xy - circle.get_pos()).length() < self.radius
