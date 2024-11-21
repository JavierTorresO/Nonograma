import pygame
from Tablero import Tablero 
from Ventana import Ventana
from menu import mostrar_menu_size

# Tamaños
CELDA_SIZE = 30
MARGIN = 40

# Colores
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
ROJO = (255, 0, 0)
BEIGE = (160, 121, 95)

class Main:
    def __init__(self):
        pygame.mixer.init()  # Inicializar el mixer de Pygame
        pygame.init()

        # Cargar sonidos
        self.sound_click = pygame.mixer.Sound("assets/sonidos/click-sound.mp3")  # al hacer clic en una celda
        self.sound_win = pygame.mixer.Sound("assets/sonidos/win-sound.mp3")  # al ganar el juego
        self.sound_board_ready = pygame.mixer.Sound("assets/sonidos/boardReady.mp3") # al iniciar el tablero

        # Cargar Imagen
        self.background_image = pygame.image.load("assets/imagen/background2.jpg") 
        
        self.screen = pygame.display.set_mode((400, 400))
        self.rows , self.cols, self.tipo = mostrar_menu_size(pygame.display.get_surface())
        self.board = Tablero(self.rows , self.cols, self.tipo)
        self.window = Ventana(self.rows, self.cols, MARGIN, CELDA_SIZE)
        self.running = True
        self.bounce_offset = 0  # Offset para el efecto de baile
        self.bounce_direction = 1  # 1 para abajo, -1 para arriba

        # Reproducir el sonido de tablero listo
        pygame.mixer.Sound.play(self.sound_board_ready)
    

    def run(self):
        while self.running:
            self.handle_events()

            background_ancho, background_alto = self.screen.get_size()  # Obtener el tamaño de la pantalla
            scaled_background = pygame.transform.scale(self.background_image, (background_ancho, background_alto))  # Escalar imagen

            self.screen.blit(scaled_background, (0, 0))

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
                if abs(self.bounce_offset) >= 6:  # Cambiar dirección
                    self.bounce_direction *= -1

                # Posición del texto con el efecto de baile
                x, y = pygame.display.get_surface().get_size()
                text_y_position = y / 2 - 40 + self.bounce_offset  # Ajustar la posición Y con el offset
                self.window.screen.blit(win_text, (x / 2 - 80, text_y_position))

            self.window.update()

    def handle_events(self):
        self.last_cell = None  # Almacena la última celda marcada

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo del mouse
                    self.last_cell = None  # Reiniciar al iniciar un nuevo clic
                    self.handle_cell_click(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:  # Si el botón izquierdo está presionado
                    self.handle_cell_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.return_to_menu()  # Volver al menú cuando se presiona Escape

    def handle_cell_click(self, mouse_pos):
        pos_x = (mouse_pos[0] - (MARGIN + 100)) // CELDA_SIZE
        pos_y = (mouse_pos[1] - (MARGIN + 100)) // CELDA_SIZE
        pos = (pos_x, pos_y)

        # Verificar si el clic está dentro de los límites del tablero
        if 0 <= pos_x < self.cols and 0 <= pos_y < self.rows:
            # Solo modificar si la celda es diferente a la última marcada
            if pos != self.last_cell:
                cell = self.board.get_cell(pos)
                if cell:
                    cell.toggle()
                    self.last_cell = pos  # Actualizar la última celda marcada

                    # Reproducir el sonido de clic en la celda
                    pygame.mixer.Sound.play(self.sound_click)

    def return_to_menu(self):
        # Volver al menu de seleccion
        self.screen = pygame.display.set_mode((400, 400))
        self.rows, self.cols, self.tipo = mostrar_menu_size(self.window.screen)
        self.window = Ventana(self.rows, self.cols, MARGIN, CELDA_SIZE)
        # Reiniciar el tablero con el nuevo tamano
        self.board = Tablero(self.rows, self.cols, self.tipo)
        if hasattr(self, "win_sound_played"):
            del (self.win_sound_played)  # Resetear para permitir el sonido de ganar en la próxima partida


if __name__ == "__main__":
    game = Main()
    game.run()
