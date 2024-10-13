import pygame
from Tablero import Tablero
from Ventana import Ventana
from menu import mostrar_menu

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
        self.rows, self.cols = mostrar_menu(self.window.screen)  # Muestra el menu y tamaño del tablero
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
        self.running = True
        self.bounce_offset = 0  # Offset para el efecto de baile
        self.bounce_direction = 1  # 1 para abajo, -1 para arriba

    def run(self):
        while self.running:
            self.handle_events()
            self.window.screen.fill((255, 255, 255))

            pygame.draw.rect(self.window.screen, (220, 220, 220), (MARGIN - 10, MARGIN - 10, 500, 300))

            self.board.draw(self.window.screen)

            if self.board.check_win():
                font = pygame.font.SysFont('Comic Sans MS', 40)
                win_text = font.render("¡Ganaste!", True, ROJO)
                # Efecto de baile
                self.bounce_offset += self.bounce_direction * 1.2
                if abs(self.bounce_offset) >= 6:  # Cambiar direccion
                    self.bounce_direction *= -1
                # Posicion del texto
                text_y = MARGIN + 200 + self.bounce_offset
                self.window.screen.blit(win_text, (MARGIN + 170, text_y))

            self.window.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
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
        # Reiniciar el tablero con el nuevo tamano
        self.board = Tablero(self.rows, self.cols, self.hints, self.solution)


if __name__ == "__main__":
    game = Main()
    game.run()