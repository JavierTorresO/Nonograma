class Celda:
    def __init__(self, position):
        self.is_filled = False
        self.position = position

    def toggle(self):
        self.is_filled = not self.is_filled
