import pygame
from Celda import Celda

NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
ROJO = (255, 0, 0)

CELDA_SIZE = 30
MARGIN = 40


class Tablero:  
    def __init__(self, rows, cols, tipo):
        self.rows = rows
        self.cols = cols
        self.tipo = tipo
        self.cells = [[Celda((x, y)) for y in range(self.cols)] for x in range(self.rows)]
        self.hints, self.solution = seleccionar_nanograma(self.rows, self.cols, self.tipo)


    def draw(self, screen):
        start_x = MARGIN + 100
        start_y = MARGIN + 50

        # Dibujar pistas de las filas
        for i, pista in enumerate(self.hints[0]):
            pista_text = " ".join(map(str, pista))
            font = pygame.font.SysFont("Comic Sans MS", 20)
            text_surface = font.render(pista_text, True, NEGRO)
            screen.blit(text_surface, (10, start_y + i * CELDA_SIZE))

        # Dibujar pistas de las columnas
        for j, pista in enumerate(self.hints[1]):
            for k, numero in enumerate(pista):
                font = pygame.font.SysFont("Comic Sans MS", 20)
                text_surface = font.render(str(numero), True, NEGRO)
                screen.blit(text_surface, (start_x + j * CELDA_SIZE + 5, 10 + (k * 30)))

        for fila in range(self.rows):  # dibujar las celdas
            for columna in range(self.cols):
                color = (DARK_GRAY if self.cells[fila][columna].is_filled else (255, 255, 255))
                pygame.draw.rect(screen, color, [(start_x + columna * CELDA_SIZE), (start_y + fila * CELDA_SIZE), CELDA_SIZE, CELDA_SIZE])
                pygame.draw.rect(screen, NEGRO, [(start_x + columna * CELDA_SIZE), (start_y + fila * CELDA_SIZE), CELDA_SIZE, CELDA_SIZE] , 1)

    def get_cell(self, pos):
        x, y = pos
        return self.cells[y][x] if 0 <= x < self.cols and 0 <= y < self.rows else None

    def check_win(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cells[i][j].is_filled != self.solution[i][j]:
                    return False
        return True


def seleccionar_nanograma(rows, cols, tipo):
    if rows == 5 and cols == 5:
        if tipo == 1:
            hints = (
                [[1, 1], [1, 1, 1], [1, 1], [1, 1], [1]],  # Pistas horizontales
                [[2], [1, 1], [1, 1], [1, 1], [2]]  # Pistas verticales
            )

            solution = [ #ejemplo1 de 5x5: corazon
                [0, 1, 0, 1, 0],
                [1, 0, 1, 0, 1],
                [1, 0, 0, 0, 1],
                [0, 1, 0, 1, 0],
                [0, 0, 1, 0, 0],
            ]
            return hints, solution
        else: 
            hints = (
                [[1, 1, 1], [1, 1], [1, 1, 1], [1, 1], [1, 1, 1]],  # Pistas horizontales
                [[1, 1, 1], [1, 1], [1, 1, 1], [1, 1], [1, 1, 1]]  # Pistas verticales
            )

            solution = [ #ejemplo2 de 5x5: ajedrez
                [1, 0, 1, 0, 1],
                [0, 1, 0, 1, 0],
                [1, 0, 1, 0, 1],
                [0, 1, 0, 1, 0],
                [1, 0, 1, 0, 1],
            ]   
            return hints, solution
    elif rows == 10 and cols == 10:
        if tipo == 1:
            hints = (
                [[4], [6], [8], [10], [1, 2, 1], [1, 2, 1], [8], [8], [3, 3], [3, 3]],  # Pistas horizontales
                [[1], [8], [4, 3], [4, 4], [7], [7], [4, 4], [4, 3], [8], [1]],  # Pistas verticales
            )

            solution = [ #ejemplo1 de 10x10: casa
                [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 0, 0, 1, 1, 0, 0, 1, 0],
                [0, 1, 0, 0, 1, 1, 0, 0, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
                [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
            ]
            return hints, solution
        else:
            hints = (
                [[4], [8], [10], [1, 1, 2, 1, 1], [1, 1, 2, 1, 1], [1, 6, 1], [6], [2, 2], [4], [2]],  # Pistas horizontales
                [[4], [2], [7], [3,4], [7,2], [7,2], [3,4], [7], [2], [4]]  # Pistas verticales
            )

            solution = [ #ejemplo2 de 10x10: perro
                [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
                [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
                [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
                [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
            ]
            return hints, solution
    if rows == 15 and cols == 15:
        if tipo == 1:
            hints = (
                [[15], [7, 7], [2,4,4,2], [3,7,3], [5,5], [4, 4], [4, 1,1,4], [1,1,1,1], [4,4], [4,3,4], [5, 5], [3,7,3], [2,4,4,2], [7,7], [15]],  # Pistas horizontales
                [[15], [7,7], [2,4,4,2], [3,7,3], [5,5], [4,4], [4, 1,1,4], [1,1,1,1,1], [4,1,1,4], [4,4], [5,5], [3,7,3], [2,4,4,2], [7,7], [15]]  # Pistas verticales
            )

            solution = [ #ejemplo1 de 15x15: sol feliz
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
                [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                [1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1],
                [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                [1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            ]
            return hints, solution
        else:
            hints = (
                [[3], [5], [4,3], [7], [5], [3], [5], [1,8], [3,3,3], [7, 3, 2], [5,4,2], [8,2], [10], [2,3], [6]],           # Pistas horizontales
                [[3], [4], [5], [4], [5], [6], [3,2,1], [2,2,5], [4,2,6], [8,2,3], [8,2,1,1], [2,6,2,1], [4,6], [2,4], [1]]   # Pistas verticales
            )
            solution = [ # ejemplo2 de 15x15: pato
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
                [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0],
                [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0],
                [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
            ]
            return hints, solution
    if rows == 20 and cols == 20:
        if tipo == 1:
            hints = (
                [[9], [2,1,1,1,1], [2,1,1,1,1], [1,1,1,1], [1,6], [1,1,3,4,2], [2,2,5,5,1], [4,1,3,2,3], [2,1,3,1,3,2], [1,1,3,1,3,2], [2,1,3,1,3,2], [2,1,3,1,3,2], [2,1,3,1,3,2], [2,1,3,1,3,3], [2,1,3,1,9], [2,1,3,1,9], [2,1,3,1,8], [1,3,1,3,2], [5,6], [10]],  # Pistas horizontales
                [[5,1,8], [2,11,1], [1,1,1,1,3], [1,1,13], [2,1,2,3], [1,1,9,2], [2,1,11,1], [1,1,2,9,2], [2,3,3], [1,14], [1,2,3], [1,1,2,9,2], [1,1,12], [16], [3,3], [1,1,3], [1,1,3], [1,2,4], [2,10], [11]]  # Pistas verticales
            )

            solution = [ #ejemplo1 de 20x20: cerveza
                [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
                [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
                [1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1],
                [1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
                [0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1],
                [1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1],
                [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1],
                [1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1],
                [1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1],
                [1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1],
                [1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1],
                [1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
            return hints, solution
        else:
            hints = (
                [[4], [1,1,1], [2,1,4,1], [1, 1, 1,1,1], [3,1,1,1,1], [1,1,1,1,1], [3,1,1,1], [1,1,1], [1, 10], [1,2,6,2], [1,1,3,3,1], [1,4,4], [1,4,4], [3,5,5], [2,2,5,5], [3,1,4,4], [5,4,4], [3,1,2,2,1], [2,6,2], [8,10]],  # Pistas horizontales
                [[3,1], [5,1], [13,3,1], [1,1,1,2,2,1], [1,1,3,1], [1], [1], [1], [10], [2,6,2], [4,1,8,1], [1,1,12], [1,4,3,2,2], [1, 1,2,2], [1,1,2,2], [1,9,2,2], [1,12], [7,8,1], [2,6,2], [10]]  # Pistas verticales
            )

            solution = [ #ejemplo2 de 20x20: llave y candado
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1],
                [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1],
                [0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
                [0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
                [0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
                [1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
                [1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
                [0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            ]
            return hints, solution

    
