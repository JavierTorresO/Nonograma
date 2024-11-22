class Celda:
    def __init__(self, position):
        self.is_filled = False
        self.is_x = False
        self.position = position

    def mark_x(self):
        self.is_x = True

    def paint(self):
        self.is_filled = True
