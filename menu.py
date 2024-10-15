import pygame # type: ignore
import sys

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)

class menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.opciones = ['1. Tableros 5x5', '2. Tableros 10x10', 'Salir']
        self.seleccion = 0
        self.option_rects = []

    def mostrar_menu(self):
        pygame.display.set_caption('Nuestro Nonogram!!!')

        while True:
            self.screen.fill(BLANCO)
            mouse_pos = pygame.mouse.get_pos()
            self.option_rects.clear()  # Limpiar la lista en cada frame

            for i, opcion in enumerate(self.opciones):
                color = ROJO if i == self.seleccion else NEGRO
                text_surface = self.font.render(opcion, True, color)
                text_rect = text_surface.get_rect(topleft=(100, 100 + i * 50))
                self.option_rects.append(text_rect)

                if text_rect.collidepoint(mouse_pos):
                    text_surface = self.font.render(opcion, True, ROJO)  # Color rojo si el mouse está sobre la opción
                    self.seleccion = i

                self.screen.blit(text_surface, text_rect)

            pygame.display.flip()

            # Manejar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.seleccion = (self.seleccion + 1) % len(self.opciones)
                    elif event.key == pygame.K_UP:
                        self.seleccion = (self.seleccion - 1) % len(self.opciones)
                    elif event.key == pygame.K_RETURN:
                        return self.seleccionar_opcion(self.seleccion)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Botón izquierdo
                        for i, rect in enumerate(self.option_rects):
                            if rect.collidepoint(event.pos):
                                return self.seleccionar_opcion(i)

    # Retorna el tamaño del tablero según la opción seleccionada
    def seleccionar_opcion(self, seleccion):
        if seleccion == 0:
            return (5, 5)
        if seleccion == 1:
            return (10, 10)
        if seleccion == 2:
            pygame.quit()
            sys.exit()
