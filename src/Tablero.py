import pygame
from Celda import Celda


NEGRO = (0, 0, 0)
BLANCO=(255,255,255)
GRIS = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
ROJO = (222, 10, 10)
AMARILLO = (200, 200, 30)
CELDA_SIZE = 30
MARGIN = 50


class Tablero:
    def __init__(self, rows, cols, tipo, mode):
        self.rows = rows
        self.cols = cols
        self.tipo = tipo
        self.mode = mode
        self.cells = [[Celda((x, y)) for y in range(self.cols)] for x in range(self.rows)]
        self.hints, self.solution = seleccionar_nanograma(self.rows, self.cols, self.tipo, self.mode)


    def draw(self, screen):
        start_x = MARGIN + 100
        start_y = MARGIN + 100

        # Dibujar pistas de las filas con colores
        for i, pista in enumerate(self.hints[0]):
            x = 10
            y = start_y + i * CELDA_SIZE
            for numero, color in pista:
                font = pygame.font.SysFont("Comic Sans MS", 30)
                text_surface = font.render(str(numero), True, ROJO if color == 2 else AMARILLO if color == 3 else NEGRO)
                screen.blit(text_surface, (x, y))
                x += 20

        # Dibujar pistas de las columnas con colores
        for j, pista in enumerate(self.hints[1]):
            x = start_x + j * CELDA_SIZE + 5
            y = 10
            for numero, color in pista:
                font = pygame.font.SysFont("Comic Sans MS", 30)
                text_surface = font.render(str(numero), True, ROJO if color == 2 else AMARILLO if color == 3 else NEGRO)
                screen.blit(text_surface, (x, y))
                y += 20


        # Dibujar las celdas
        for fila in range(self.rows):
            for columna in range(self.cols):
                cell = self.cells[fila][columna]
                x = start_x + columna * CELDA_SIZE
                y = start_y + fila * CELDA_SIZE

                # Determinar el color de la celda
                if cell.is_x:
                    color = BLANCO
                elif cell.is_color == 2:
                    color = ROJO
                elif cell.is_color == 3:
                    color = AMARILLO
                else:
                    color = DARK_GRAY if cell.is_painted else BLANCO

                # Dibujar el fondo de la celda
                pygame.draw.rect(screen, color, [x, y, CELDA_SIZE, CELDA_SIZE])

                # Dibujar el borde de la celda
                pygame.draw.rect(screen, NEGRO, [x, y, CELDA_SIZE, CELDA_SIZE], 1)

                # Dibujar la "X" si está marcada
                if cell.is_x:
                    pygame.draw.line(screen, NEGRO, (x, y), (x + CELDA_SIZE, y + CELDA_SIZE), 2)
                    pygame.draw.line(screen, NEGRO, (x + CELDA_SIZE, y), (x, y + CELDA_SIZE), 2)

        # Dibujar interfaz del modo "dos colores" si aplica
        if self.mode == "dos_colores":
            overlay = pygame.Surface((screen.get_width(), 70), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 90))  # Negro con 35% de transparencia (90 de 255)
            screen.blit(overlay, (0, screen.get_height() - 70))

            font = pygame.font.SysFont("Comic Sans MS", 35)
            text_surface = font.render("Colores:", True, NEGRO)
            screen.blit(text_surface, ((start_x + ((CELDA_SIZE * self.cols)/2) - 93)/2 - 40, screen.get_height() - 45))
            font = pygame.font.SysFont("Time New Roman", 27)

            # Dibujar dos cuadrados con colores distintos
            pygame.draw.rect(screen, NEGRO, (start_x + ((CELDA_SIZE * self.cols)/2) - 93, screen.get_height() - 53, 86, 36))
            pygame.draw.rect(screen, ROJO, (start_x + ((CELDA_SIZE * self.cols)/2) - 90, screen.get_height() - 50, 80, 30))
            text_surface = font.render("press 1", True, NEGRO)
            screen.blit(text_surface, (start_x + ((CELDA_SIZE * self.cols)/2) - 80, screen.get_height() - 45))


            pygame.draw.rect(screen, NEGRO, (start_x + ((CELDA_SIZE * self.cols)/2) + 7, screen.get_height() - 53, 86, 36))
            pygame.draw.rect(screen, AMARILLO, (start_x + ((CELDA_SIZE * self.cols)/2) + 10, screen.get_height() - 50, 80, 30))
            text_surface = font.render("press 2", True, NEGRO)
            screen.blit(text_surface, (start_x + ((CELDA_SIZE * self.cols)/2) + 20, screen.get_height() - 45))


    def get_cell(self, pos):
        x, y = pos
        return self.cells[y][x] if 0 <= x < self.cols and 0 <= y < self.rows else None

    def check_win(self):
        for i in range(self.rows):
            for j in range(self.cols):

                if self.mode == "clasico":
                    if self.cells[i][j].is_painted != self.solution[i][j]:
                        return False

                else:
                    if self.solution[i][j] == 0:
                        # La celda debe estar sin pintar (vacía)
                        if self.cells[i][j].is_painted:
                            return False
                    elif self.solution[i][j] == 2:
                        # La celda debe estar pintada con el primer color
                        if self.cells[i][j].is_color != 2:
                            return False
                    elif self.solution[i][j] == 3:
                        # La celda debe estar pintada con el segundo color
                        if self.cells[i][j].is_color != 3:
                            return False

        return True

    
def generar_pistas(solution):
    pistas_horizontales = []
    pistas_verticales = []
    
    # Generar pistas horizontales
    for row in solution:
        pistas = []
        current_color = None
        count = 0
        for celda in row:
            if celda > 0:  # Ignorar celdas vacías
                if celda == current_color:
                    count += 1
                else:
                    if current_color is not None:  # Guardar el segmento anterior
                        pistas.append((count, current_color))
                    current_color = celda
                    count = 1
            else:  # Celda vacía
                if current_color is not None:
                    pistas.append((count, current_color))
                    current_color = None
                    count = 0
        if current_color is not None:  # Guardar último segmento
            pistas.append((count, current_color))
        pistas_horizontales.append(pistas)
    
    # Generar pistas verticales
    for col in range(len(solution[0])):
        pistas = []
        current_color = None
        count = 0
        for row in solution:
            celda = row[col]
            if celda > 0:  # Ignorar celdas vacías
                if celda == current_color:
                    count += 1
                else:
                    if current_color is not None:  # Guardar el segmento anterior
                        pistas.append((count, current_color))
                    current_color = celda
                    count = 1
            else:  # Celda vacía
                if current_color is not None:
                    pistas.append((count, current_color))
                    current_color = None
                    count = 0
        if current_color is not None:  # Guardar último segmento
            pistas.append((count, current_color))
        pistas_verticales.append(pistas)

    return pistas_horizontales, pistas_verticales


def seleccionar_nanograma(rows, cols, tipo, mode):
    if mode == "clasico":
        if rows == 5 and cols == 5:
            if tipo == 1:

                solution = [ #ejemplo1 de 5x5: corazon
                    [0, 1, 0, 1, 0],
                    [1, 0, 1, 0, 1],
                    [1, 0, 0, 0, 1],
                    [0, 1, 0, 1, 0],
                    [0, 0, 1, 0, 0],
                ]

                hints = generar_pistas(solution)

                return hints, solution
            else:
                
                solution = [ #ejemplo2 de 5x5: ajedrez
                    [1, 0, 1, 0, 1],
                    [0, 1, 0, 1, 0],
                    [1, 0, 1, 0, 1],
                    [0, 1, 0, 1, 0],
                    [1, 0, 1, 0, 1],
                ]

                hints = generar_pistas(solution)

                return hints, solution
        elif rows == 10 and cols == 10:
            if tipo == 1:

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

                hints = generar_pistas(solution)

                return hints, solution
            else:
                
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

                hints = generar_pistas(solution)

                return hints, solution
        if rows == 15 and cols == 15:
            if tipo == 1:
            
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

                hints = generar_pistas(solution)

                return hints, solution
            else:
                
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

                hints = generar_pistas(solution)

                return hints, solution
        if rows == 20 and cols == 20:
            if tipo == 1:

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

                hints = generar_pistas(solution)

                return hints, solution
            else:

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

                hints = generar_pistas(solution)

                return hints, solution
            
    elif mode == "dos_colores":
        if rows == 5 and cols == 5:
            if tipo == 1:

                solution = [ #ejemplo1 de 5x5: corazon
                    [3, 2, 3, 2, 3],
                    [2, 2, 2, 2, 2],
                    [2, 2, 2, 2, 2],
                    [3, 2, 2, 2, 3],
                    [3, 3, 2, 3, 3],
                ]
                hints = generar_pistas(solution)

                return hints, solution
            else: 
                
                solution = [ #ejemplo2 de 5x5: ajedrez
                    [2, 3, 2, 3, 2],
                    [3, 2, 3, 2, 3],
                    [2, 3, 2, 3, 2],
                    [3, 2, 3, 2, 3],
                    [2, 3, 2, 3, 2],
                ]

                hints = generar_pistas(solution)

                return hints, solution
        elif rows == 10 and cols == 10:
            if tipo == 1:

                solution = [ #ejemplo1 de 10x10: casa
                    [0, 0, 0, 2, 2, 2, 2, 0, 0, 0],
                    [0, 0, 2, 2, 2, 2, 2, 2, 0, 0],
                    [0, 2, 2, 2, 2, 2, 2, 2, 2, 0],
                    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2], 
                    [0, 3, 0, 0, 3, 3, 0, 0, 3, 0],
                    [0, 3, 0, 0, 3, 3, 0, 0, 3, 0],
                    [0, 3, 3, 3, 3, 3, 3, 3, 3, 0],
                    [0, 3, 3, 3, 3, 3, 3, 3, 3, 0],
                    [0, 3, 3, 3, 0, 0, 3, 3, 3, 0],
                    [0, 3, 3, 3, 0, 0, 3, 3, 3, 0],
                ]

                hints = generar_pistas(solution)

                return hints, solution
            else:

                solution = [ #ejemplo2 de 10x10: rombo amarillo
                    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                    [2, 2, 2, 2, 3, 3, 2, 2, 2, 2],
                    [2, 2, 2, 3, 3, 3, 3, 2, 2, 2],
                    [2, 2, 3, 3, 3, 3, 3, 3, 2, 2],
                    [2, 3, 3, 3, 3, 3, 3, 3, 3, 2],
                    [2, 3, 3, 3, 3, 3, 3, 3, 3, 2],
                    [2, 2, 3, 3, 3, 3, 3, 3, 2, 2],
                    [2, 2, 2, 3, 3, 3, 3, 2, 2, 2],
                    [2, 2, 2, 2, 3, 3, 2, 2, 2, 2],
                    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                ]

                hints = generar_pistas(solution)

                return hints, solution
