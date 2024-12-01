class Celda:
    def __init__(self, position):
        self.is_painted = False     # Indica si la celda está pintada
        self.is_x = False           # Indica si la celda tiene una "X"
        self.position = position    # Guarda la posición de la celda
        self.is_locked = False      # Indica si la celda está bloqueada
        self.is_color = 0

    def __str__(self):
        return str(self.is_color)
    
    # def toggle(self):
    #     self.is_painted = not self.is_painted #cambia una celda entre pintado-nopintado

    def toggle_x(self):
        self.is_x = not self.is_x #cambia el estado de la "X" en una celda

    # def toggle_color1(self):
    #     if self.is_color1 == 2:
    #         self.is_color1 = 0
    #     else:
    #         self.is_color1 = 2
    #     self.is_painted = not self.is_painted
    
    # def toggle_color2(self):
    #     if self.is_color2 == 3:
    #         self.is_color1 = 0
    #     else:
    #         self.is_color1 = 3
        # self.is_painted = not self.is_painted
