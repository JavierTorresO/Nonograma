import pygame
from Tablero import Tablero 
from Ventana import Ventana
from menu import mostrar_menu_home

# Tamaños
CELDA_SIZE = 30
MARGIN = 50

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
        self.color = None

        # Cargar sonidos
        self.sound_click = pygame.mixer.Sound("assets/sonidos/click-sound.mp3")  # al hacer clic en una celda
        self.sound_win = pygame.mixer.Sound("assets/sonidos/win-sound.mp3")  # al ganar el juego
        self.sound_board_ready = pygame.mixer.Sound("assets/sonidos/boardReady.mp3") # al iniciar el tablero

        # Cargar Imagen
        self.background_image = pygame.image.load("assets/imagen/background2.jpg") 
        
        self.screen = pygame.display.set_mode((400, 400))  # crea una ventana inicial para el juego  
        self.rows , self.cols, self.tipo, self.mode = mostrar_menu_home(pygame.display.get_surface())  # nos muestra las opciones y nos devuelve las filas, columnas y cual nanograma elejimos
        self.board = Tablero(self.rows , self.cols, self.tipo, self.mode) # tablero recupera las pistas y la solucion del nanograma que elejimos y crea el tablero de juego
        self.window = Ventana(self.rows, self.cols, self.mode, MARGIN, CELDA_SIZE) # crea la ventana de juego segun el nanograma elejido
        self.running = True
        self.bounce_offset = 0  # Offset para el efecto de baile
        self.bounce_direction = 1  # 1 para abajo, -1 para arriba
        self.last_cell = None  # Guardar la última celda marcada
        self.initial_paint_state = None  # Inicializar el estado inicial de la celda

        # Reproducir el sonido de tablero listo
        pygame.mixer.Sound.play(self.sound_board_ready)
    

    def run(self):
        while self.running:
            self.handle_events()

            background_ancho, background_alto = self.screen.get_size()  # Obtener el tamaño del fondo para la ventana
            scaled_background = pygame.transform.scale(self.background_image, (background_ancho, background_alto))  # Escalar imagen

            self.screen.blit(scaled_background, (0, 0))

            self.board.draw(self.window.screen)

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
                    self.last_cell = None  # Reiniciar al iniciar un nuevo clic
                    self.initial_paint_state = self.get_cell_paint_state(event.pos)  # Obtener el estado inicial de la celda
                    self.handle_cell_click(event.pos, self.color, lock=True)
                elif event.button == 3:  # Botón derecho del mouse (clic para marcar X)
                    self.last_cell = None  # Reiniciar al iniciar un nuevo clic
                    self.handle_right_click(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Botón izquierdo del mouse
                    self.unlock_all_cells()
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:  # Si el botón izquierdo está presionado
                    self.handle_cell_click(event.pos, self.color)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.return_to_menu()  # Volver al menú cuando se presiona Escape
                if self.mode == "dos_colores":
                    if event.key == pygame.K_1:
                        self.color = 1
                        # print(self.color)
                        pygame.mixer.Sound.play(self.sound_click)    
                    if event.key == pygame.K_2:
                        self.color = 2
                        # print(self.color)
                        pygame.mixer.Sound.play(self.sound_click)
                    if event.key == pygame.K_3:
                        self.board.imprimir_cells()
                    if event.key == pygame.K_4:
                        self.board.imprimir_solution()
                

    def handle_cell_click(self, mouse_pos, color=None, lock=False):
        pos_x = (mouse_pos[0] - (MARGIN + 100)) // CELDA_SIZE
        pos_y = (mouse_pos[1] - (MARGIN + 100)) // CELDA_SIZE
        pos = (pos_x, pos_y)
    
        # Verificar si el clic está dentro de los límites del tablero
        if 0 <= pos_x < self.cols and 0 <= pos_y < self.rows:
            if pos != self.last_cell:  # Solo modificar si la celda es diferente a la última marcada
                cell = self.board.get_cell(pos)
                if cell and not cell.is_locked and not cell.is_x:  # No permitir pintar si la celda está bloqueada
                    if self.initial_paint_state:  # Si la celda inicial estaba marcada
                        # Desmarcar la celda y resetear colores
                        cell.is_painted = False
                        cell.is_color = 0
                        pygame.mixer.Sound.play(self.sound_click)  # Sonido al desmarcar
                    else:
                        if color == 1:  # Pintar con el primer color
                            print("Pintando con color 1")
                            cell.is_color = 2
                            cell.is_painted = True
                            pygame.mixer.Sound.play(self.sound_click)  # Sonido al pintar con color 1
                        elif color == 2:  # Pintar con el segundo color
                            print("Pintando con color 2")
                            cell.is_color = 3
                            cell.is_painted = True
                            pygame.mixer.Sound.play(self.sound_click)  # Sonido al pintar con color 2
                        else:  # Pintar sin especificar color (modo clásico)
                            cell.is_painted = True
                            pygame.mixer.Sound.play(self.sound_click)  # Sonido al pintar en modo clásico
    
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
        self.color = None
        self.win_time = None
        self.win_sound_played = False
        self.screen = pygame.display.set_mode((400, 400))
        self.rows, self.cols, self.tipo, self.mode = mostrar_menu_home(self.window.screen)
        self.window = Ventana(self.rows, self.cols, self.mode, MARGIN, CELDA_SIZE)
        self.board = Tablero(self.rows, self.cols, self.tipo, self.mode)

        # Recargar sonidos si es necesario
        self.sound_click = pygame.mixer.Sound("assets/sonidos/click-sound.mp3")
        self.sound_win = pygame.mixer.Sound("assets/sonidos/win-sound.mp3")
        self.sound_board_ready = pygame.mixer.Sound("assets/sonidos/boardReady.mp3")

        # Reproducir el sonido de tablero listo
        pygame.mixer.Sound.play(self.sound_board_ready)



if __name__ == "__main__":
    game = Main()
    game.run()
