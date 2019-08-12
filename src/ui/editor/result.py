from PyQt5.QtWidgets import QGraphicsEllipseItem


# TODO
class ResultItem(QGraphicsEllipseItem):
    radius = 10

    def __init__(self, parent, result):
        super().__init__(-self.radius, -self.radius, self.diameter, self.diameter, parent)
        self.data = result

    @property
    def diameter(self):
        return self.radius * 2
