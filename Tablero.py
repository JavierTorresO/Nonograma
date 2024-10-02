import pygame

from Celda import Celda

NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
ROJO = (255, 0, 0)

CELDA_SIZE = 30
MARGIN = 40
ROWS, COLS = 5, 5

class Tablero:
    def __init__(self, rows, cols, hints, solution):
        self.cells = [[Celda((x, y)) for y in range(cols)] for x in range(rows)]
        self.hints = hints
        self.solution = solution

    def draw(self, screen):
        start_x = MARGIN + 100
        start_y = MARGIN + 50

        # Dibujar pistas de las filas
        for i, pista in enumerate(self.hints[0]):
            pista_text = " ".join(map(str, pista))
            font = pygame.font.SysFont('Comic Sans MS', 20)
            text_surface = font.render(pista_text, True, NEGRO)
            screen.blit(text_surface, (10, start_y + i * CELDA_SIZE))

        # Dibujar pistas de las columnas
        for j, pista in enumerate(self.hints[1]):
            for k, numero in enumerate(pista):
                font = pygame.font.SysFont('Comic Sans MS', 20)
                text_surface = font.render(str(numero), True, NEGRO)
                screen.blit(text_surface, (start_x + j * CELDA_SIZE + 5, 10 + (k * 30)))

        for fila in range(ROWS):
            for columna in range(COLS):
                color = DARK_GRAY if self.cells[fila][columna].is_filled else (255, 255, 255)
                pygame.draw.rect(screen, color, [(start_x + columna * CELDA_SIZE), (start_y + fila * CELDA_SIZE), CELDA_SIZE, CELDA_SIZE])
                pygame.draw.rect(screen, NEGRO, [(start_x + columna * CELDA_SIZE), (start_y + fila * CELDA_SIZE), CELDA_SIZE, CELDA_SIZE], 1)

    def get_cell(self, pos):
        x, y = pos
        return self.cells[y][x] if 0 <= x < len(self.cells[0]) and 0 <= y < len(self.cells) else None

    def check_win(self):
        for i in range(ROWS):
            for j in range(COLS):
                if self.cells[i][j].is_filled != self.solution[i][j]:
                    return False
        return True

