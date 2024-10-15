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
        pygame.mixer.init()  # Inicializar el mixer de Pygame
        pygame.init()

        # Cargar sonidos
        self.sound_click = pygame.mixer.Sound("click-sound.mp3")  # al hacer clic en una celda
        self.sound_win = pygame.mixer.Sound("win-sound.mp3")  # al ganar el juego

        self.screen = pygame.display.set_mode((400, 400))
        self.rows, self.cols = mostrar_menu(pygame.display.get_surface())  # Muestra el menu y tamaño del tablero

        self.window = Ventana(self.rows, self.cols, MARGIN, CELDA_SIZE)

        self.hints = (
            [[1, 1], [1, 1, 1], [1, 1], [1, 1], [1]],  # Pistas horizontales
            [[2], [1, 1], [1, 1], [1, 1], [2]],  # Pistas verticales
        )
        self.solution = [
            [0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 0],
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
                font = pygame.font.SysFont("Comic Sans MS", 40)
                win_text = font.render("¡Ganaste!", True, ROJO)

                # Reproducir el sonido de ganar 
                if not hasattr(self, "win_sound_played"):
                    pygame.mixer.Sound.play(self.sound_win)
                    self.win_sound_played = True

                # Efecto de baile
                self.bounce_offset += self.bounce_direction * 1.2
                if abs(self.bounce_offset) >= 6:  # Cambiar direccion
                    self.bounce_direction *= -1
                # Posicion del texto
                x, y = pygame.display.get_surface().get_size()
                print(x,y)
                self.window.screen.blit(win_text, (x/2-80, y/2-40))

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

                        # Reproducir el sonido de clic en la celda
                        pygame.mixer.Sound.play(self.sound_click)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.return_to_menu()  # Volver al menu cuando se presiona Escape

    def return_to_menu(self):
        # Volver al menu de seleccion
        self.screen = pygame.display.set_mode((400, 400))
        self.rows, self.cols = mostrar_menu(self.window.screen)
        self.window = Ventana(self.rows, self.cols, MARGIN, CELDA_SIZE)
        # Reiniciar el tablero con el nuevo tamano
        self.board = Tablero(self.rows, self.cols, self.hints, self.solution)
        if hasattr(self, "win_sound_played"):
            del (self.win_sound_played)  # Resetear para permitir el sonido de ganar en la próxima partida


if __name__ == "__main__":
    game = Main()
    game.run()
