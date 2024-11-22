class Celda:
    def __init__(self, position):
        self.is_filled = False  # Celda activada
        self.is_marked_x = False  # Estado de "X"
        self.position = position

    def toggle(self):
        self.is_filled = not self.is_filled  # Cambia entre marcado y no marcado

    def toggle_x(self):
        self.is_marked_x = not self.is_marked_x  # Cambia entre marcado con X y no marcado
