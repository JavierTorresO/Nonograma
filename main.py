import pygame
from Tablero import Tablero
from Ventana import Ventana
from menu import mostrar_menu
from MenuNanogramas import mostrar_menu_nanogramas  # Asegurate de tener este modulo

# Tamaños
CELDA_SIZE = 30
MARGIN = 40

# Colores
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
ROJO = (255, 0, 0)

class Main:
    def __init__(self):
        self.window = Ventana(600, 400)
        self.rows, self.cols = mostrar_menu(self.window.screen)  # Muestra el menu y tamano del tablero
        self.hints = None
        self.solution = None
        self.board = None
        self.running = True
        self.bounce_offset = 0
        self.bounce_direction = 1
        
        # Selecciona el nanograma despues de establecer el tamano
        self.seleccionar_nanograma()

    def seleccionar_nanograma(self):
        # Muestra el menu de nanogramas
        nanograma = mostrar_menu_nanogramas(self.window.screen, self.rows, self.cols)
        if nanograma is None:
            self.return_to_menu()  # Volver al menu si se selecciona "Volver"
            return
        # Asigna el mismo nanograma cada vez que se selecciona
        self.hints = (
            [[1, 1], [1, 1, 1], [1, 1], [1, 1], [1]],  # Pistas horizontales
            [[2], [1, 1], [1, 1], [1, 1], [2]]  # Pistas verticales
        )
        self.solution = [
            [0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 0]
        ]  # Tablero solucion
        self.board = Tablero(self.rows, self.cols, self.hints, self.solution)

    def run(self):
        while self.running:
            self.handle_events()
            self.window.screen.fill((255, 255, 255))
            pygame.draw.rect(self.window.screen, (220, 220, 220), (MARGIN - 10, MARGIN - 10, 500, 300))
            if self.board:
                self.board.draw(self.window.screen)

            if self.board and self.board.check_win():
                font = pygame.font.SysFont('Comic Sans MS', 40)
                win_text = font.render("¡Ganaste!", True, ROJO)
                self.bounce_offset += self.bounce_direction * 1.2
                if abs(self.bounce_offset) >= 6:
                    self.bounce_direction *= -1
                text_y = MARGIN + 200 + self.bounce_offset
                self.window.screen.blit(win_text, (MARGIN + 170, text_y))

            self.window.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.board:  # Asegurate de que el tablero este definido
                    pos = ((event.pos[0] - (MARGIN + 100)) // CELDA_SIZE, (event.pos[1] - (MARGIN + 50)) // CELDA_SIZE)
                    cell = self.board.get_cell(pos)
                    if cell:
                        cell.toggle()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.return_to_menu()  # Volver al menu cuando se presiona Escape

    def return_to_menu(self):
        # Volver al menu de seleccion 
        self.rows, self.cols = mostrar_menu(self.window.screen)
        self.seleccionar_nanograma()  # Llama a la funcion para seleccionar el nanograma

if __name__ == "__main__":
    game = Main()
    game.run()
