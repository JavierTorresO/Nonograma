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
GRIS_OSCURO = (150, 150, 150)
ROJO = (255, 0, 0)
BEIGE = (160, 121, 95)
    
class Main:
    def __init__(self):
        self.win_time = None  # Atributo para almacenar el tiempo de victoria
        self.win_sound_played = False  # Atributo para controlar si el sonido de victoria se ha reproducido
        pygame.mixer.init()  # Inicializar el mixer de Pygame
        pygame.init()      # Inicializar oygam

        # Cargar sonidos
        self.sound_click = pygame.mixer.Sound("assets/sonidos/click-sound.mp3")  # al hacer clic en una celda
        self.sound_win = pygame.mixer.Sound("assets/sonidos/win-sound.mp3")  # al ganar el juego
        self.sound_board_ready = pygame.mixer.Sound("assets/sonidos/boardReady.mp3") # al iniciar el tablero
        self.sound_resetbutton = pygame.mixer.Sound("assets/sonidos/resetbutton.mp3") # click en boton de restear el tablero

        # Cargar Imagen
        self.background_image = pygame.image.load("assets/imagen/background2.jpg") 
        
        self.screen = pygame.display.set_mode((400, 400))  # crea una ventana inicial para el juego  
        self.rows , self.cols, self.tipo = mostrar_menu_size(pygame.display.get_surface())  # nos muestra las opciones y nos devuelve las filas, columnas y cual nanograma elejimos
        self.board = Tablero(self.rows , self.cols, self.tipo) # tablero recupera las pistas y la solucion del nanograma que elejimos y crea el tablero de juego
        self.window = Ventana(self.rows, self.cols, MARGIN, CELDA_SIZE) # crea la ventana de juego segun el nanograma elejido
        self.running = True
        self.bounce_offset = 0  # Offset para el efecto de baile
        self.bounce_direction = 1  # 1 para abajo, -1 para arriba
        self.last_cell = None  # Guardar la última celda marcada
        self.initial_paint_state = None  # Inicializar el estado inicial de la celda

        # Reproducir el sonido de tablero listo
        pygame.mixer.Sound.play(self.sound_board_ready)

        # Boton de reinicio
        self.reset_button = pygame.Rect(6, 10, 90, 30) # Posicion y tamaño del boton

    def draw_reset_button(self):
        pygame.draw.rect(self.window.screen, BEIGE, self.reset_button, border_radius=10)  # Dibujar el botón
        font = pygame.font.SysFont("Comic Sans MS", 20)
        text = font.render("Reiniciar", True, NEGRO)
        text_rect = text.get_rect(center = self.reset_button.center)
        self.window.screen.blit(text, (10,10))

    

    def run(self):
        while self.running:
            self.handle_events()

            background_ancho, background_alto = self.screen.get_size()  # Obtener el tamaño del fondo para la ventana
            scaled_background = pygame.transform.scale(self.background_image, (background_ancho, background_alto))  # Escalar imagen

            self.screen.blit(scaled_background, (0, 0))

            self.board.draw(self.window.screen)
            self.draw_reset_button() # Dibuja el boton de reinicio

            if self.board.check_win():
                if not self.win_time:
                    self.win_time = pygame.time.get_ticks()  # Guardar el tiempo de victoria
                    if not self.win_sound_played:
                        pygame.mixer.Sound.play(self.sound_win)
                        self.win_sound_played = True

                font = pygame.font.SysFont("Comic Sans MS", 60)
                win_text = font.render("¡Ganaste!", True, ROJO)

                # Efecto de baile
                self.bounce_offset += self.bounce_direction * 1.2
                if abs(self.bounce_offset) >= 6:  # Cambiar dirección
                    self.bounce_direction *= -1

                # Posicion del texto con el efecto de baile
                x, y = pygame.display.get_surface().get_size()
                text_width, text_height = win_text.get_size()
                self.window.screen.blit(win_text, (x / 2 - text_width / 2, y / 2 - text_height + self.bounce_offset))

                # Verificar si han pasado 3 segundos desde la victoria
                if pygame.time.get_ticks() - self.win_time >= 3000:
                    self.return_to_menu()  # Volver al menú despues de e segundos


            self.window.update()

    
    def handle_events(self):
        if self.win_time:  # No manejar eventos si se ha ganado
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Boton izquierdo del mouse
                    if self.reset_button.collidepoint(event.pos): # Si se hace clic en el botón de reinicio
                        pygame.mixer.Sound.play(self.sound_resetbutton)
                        self.reset_buttontab() # Reiniciar el tablero
                    else:
                        self.last_cell = None  # Reiniciar al iniciar un nuevo clic
                        self.initial_paint_state = self.get_cell_paint_state(event.pos)  # Obtener el estado inicial de la celda
                        self.handle_cell_click(event.pos, lock=True)
                elif event.button == 3:  # Botón derecho del mouse (clic para marcar X)
                    self.last_cell = None  # Reiniciar al iniciar un nuevo clic
                    self.handle_right_click(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Botón izquierdo del mouse
                    self.unlock_all_cells()
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:  # Si el botón izquierdo está presionado
                    self.handle_cell_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.return_to_menu()  # Volver al menú cuando se presiona Escape

    def handle_cell_click(self, mouse_pos, lock=False):
        pos_x = (mouse_pos[0] - (MARGIN + 100)) // CELDA_SIZE
        pos_y = (mouse_pos[1] - (MARGIN + 100)) // CELDA_SIZE
        pos = (pos_x, pos_y)

        # Verificar si el clic está dentro de los límites del tablero
        if 0 <= pos_x < self.cols and 0 <= pos_y < self.rows:
            if pos != self.last_cell:  # Solo modificar si la celda es diferente a la última marcada
                cell = self.board.get_cell(pos)
                if cell:
                    if not cell.is_x and not cell.is_locked:  # No permitir pintar si la celda tiene una "X" o está bloqueada
                        if self.initial_paint_state is not None:
                            if self.initial_paint_state:  # Si la celda inicial estaba marcada
                                if cell.is_painted:
                                    cell.is_painted = False  # Desmarcar la celda
                                    pygame.mixer.Sound.play(self.sound_click)  # Reproducir sonido
                            else:  # Si la celda inicial estaba desmarcada
                                if not cell.is_painted:
                                    cell.is_painted = True  # Marcar la celda
                                    pygame.mixer.Sound.play(self.sound_click)  # Reproducir sonido
                        if lock:
                            cell.is_locked = True  # Bloquear la celda si se especifica
                        self.last_cell = pos  # Actualizar la última celda marcada
                        

    def unlock_all_cells(self):
        for row in self.board.cells:
            for cell in row:
                cell.is_locked = False  # Desbloquear todas las celdas

    def get_cell_paint_state(self, mouse_pos):
        pos_x = (mouse_pos[0] - (MARGIN + 100)) // CELDA_SIZE
        pos_y = (mouse_pos[1] - (MARGIN + 100)) // CELDA_SIZE
        pos = (pos_x, pos_y)

        # Verificar si el clic está dentro de los límites del tablero
        if 0 <= pos_x < self.cols and 0 <= pos_y < self.rows:
            cell = self.board.get_cell(pos)
            if cell:
                return cell.is_painted
        return None

    def handle_right_click(self, mouse_pos):
        pos_x = (mouse_pos[0] - (MARGIN + 100)) // CELDA_SIZE
        pos_y = (mouse_pos[1] - (MARGIN + 100)) // CELDA_SIZE
        pos = (pos_x, pos_y)

        if 0 <= pos_x < self.cols and 0 <= pos_y < self.rows:
            cell = self.board.get_cell(pos)
            if cell:
                if cell.is_painted:  # Si la celda está pintada, despintarla
                    cell.is_painted = False  # Quitar la pintura
                else:
                    cell.toggle_x()  # Alternar la "X"
                pygame.mixer.Sound.play(self.sound_click)  # Reproducir sonido

    # Volver al menu de seleccion
    def return_to_menu(self):
        self.win_time = None
        self.win_sound_played = False
        self.screen = pygame.display.set_mode((400, 400))
        self.rows, self.cols, self.tipo = mostrar_menu_size(self.window.screen)
        self.window = Ventana(self.rows, self.cols, MARGIN, CELDA_SIZE)
        self.board = Tablero(self.rows, self.cols, self.tipo)

        # Recargar sonidos si es necesario
        self.sound_click = pygame.mixer.Sound("assets/sonidos/click-sound.mp3")
        self.sound_win = pygame.mixer.Sound("assets/sonidos/win-sound.mp3")
        self.sound_board_ready = pygame.mixer.Sound("assets/sonidos/boardReady.mp3")

        # Reproducir el sonido de tablero listo
        pygame.mixer.Sound.play(self.sound_board_ready)

    # Reiniciar el tablero
    def reset_buttontab(self):
        for row in self.board.cells:
            for cell in row:
                cell.is_painted = False
                cell.is_locked = False
                cell.is_x = False


if __name__ == "__main__":
    game = Main()
    game.run()
