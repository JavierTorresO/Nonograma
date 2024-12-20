class Celda:
    def __init__(self, position):
        self.is_painted = False     # Indica si la celda está pintada
        self.is_x = False           # Indica si la celda tiene una "X"
        self.position = position    # Guarda la posición de la celda
        self.is_locked = False      # Indica si la celda está bloqueada
        self.is_color = 0

    def __str__(self):
        return str(self.is_color)    

    def toggle_x(self):
        self.is_x = not self.is_x #cambia el estado de la "X" en una celda