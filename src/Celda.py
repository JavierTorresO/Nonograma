class Celda:
    def __init__(self, position):
        self.is_painted = False      # Indica si la celda está pintada
        self.is_x = False           # Indica si la celda tiene una "X"
        self.position = position    # Guarda la posición de la celda
        self.is_locked = False      # Indica si la celda está bloqueada

    def toggle(self):
        self.is_painted = not self.is_painted #cambia una celda entre pintado-nopintado

    def toggle_x(self):
        self.is_x = not self.is_x #cambia el estado de la "X" en una celda

    def hold(self):
        if not self.is_painted:
            self.is_painted = True  # Marca la celda si no está ya marcada