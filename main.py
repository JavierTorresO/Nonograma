import pygame
from Tablero import Tablero
from Ventana import Ventana
from menu import menu

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
        pygame.mixer.init()
        self.sound_click = pygame.mixer.Sound("click-sound.mp3")
        self.sound_win = pygame.mixer.Sound("win-sound.mp3")

        self.window = Ventana(800, 600)  # Ventana fija
        self.board = None
        self.running = True
        self.bounce_offset = 0
        self.bounce_direction = 1

        # Muestra el menú para seleccionar el tamaño del tablero
        self.menu = menu(self.window.screen)
        self.run_menu()

    def run_menu(self):
        size = self.menu.mostrar_menu()  # Muestra el menú y obtiene el tamaño seleccionado
        if size == (5, 5):
            self.board = Tablero.crear_tablero_chico()  # Llama a la función para crear el tablero pequeño(5x5)
        elif size == (10, 10):
            self.board = Tablero.crear_tablero_grande()  # Llama a la función para crear el tablero grande(10x10)
        self.run()

    def run(self):
        while self.running:
            self.handle_events()
            self.window.screen.fill((255, 255, 255))

            self.board.draw(self.window.screen)

            if self.board.check_win():
                font = pygame.font.SysFont("Comic Sans MS", 40)
                win_text = font.render("¡Ganaste!", True, ROJO)

                # Reproducir el sonido de ganar (solo una vez)
                if not hasattr(self, "win_sound_played"):
                    pygame.mixer.Sound.play(self.sound_win)
                    self.win_sound_played = True

                # Efecto de "baile" del texto de victoria
                self.bounce_offset += self.bounce_direction * 1.2
                if abs(self.bounce_offset) >= 6:  #cambiar dirección
                    self.bounce_direction *= -1

                # Posición del texto
                text_y = MARGIN + 200 + self.bounce_offset
                self.window.screen.blit(win_text, (MARGIN + 170, text_y))
            else:
                # Reiniciar el sonido de victoria si no se ha ganado
                if hasattr(self, "win_sound_played"):
                    del self.win_sound_played  # Resetear para permitir el sonido de ganar en la próxima partida

            self.window.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic izquierdo
                    # Obtener la posición de la celda
                    pos = ((event.pos[0] - (MARGIN + 100)) // CELDA_SIZE,
                            (event.pos[1] - (MARGIN + 50)) // CELDA_SIZE)
                    cell = self.board.get_cell(pos)
                    if cell:
                        cell.toggle()

                        # Reproducir el sonido de clic en la celda
                        pygame.mixer.Sound.play(self.sound_click)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.run_menu()  # Regresa al menú al presionar ESC

if __name__ == "__main__":
    game = Main()
    game.run()