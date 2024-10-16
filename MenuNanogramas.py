import pygame
import sys

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)

def mostrar_menu_nanogramas(screen, rows, cols):
    pygame.display.set_caption('Seleccione un Nanograma.')

    font = pygame.font.SysFont('Comic Sans MS', 30)

    # Opciones de nanogramas
    opciones = ['Nanograma 1', 'Nanograma 2', 'Volver']
    seleccion = 0

    while True:
        screen.fill(BLANCO)

        # Posicion del mouse
        mouse_pos = pygame.mouse.get_pos()

        for i, opcion in enumerate(opciones):
            if i == seleccion:
                color = ROJO  # Color rojo para la opcion seleccionada
            else:
                color = NEGRO

            # Renderizar el texto
            text_surface = font.render(opcion, True, color)
            text_rect = text_surface.get_rect(topleft=(100, 100 + i * 50))
            screen.blit(text_surface, text_rect)

            # Cambiar la seleccion con el mouse
            if text_rect.collidepoint(mouse_pos):
                seleccion = i

        pygame.display.flip()

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif event.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif event.key == pygame.K_RETURN:
                    return seleccionar_nanograma(seleccion, rows, cols)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    for i in range(len(opciones)):
                        text_rect = font.render(opciones[i], True, NEGRO).get_rect(topleft=(100, 100 + i * 50))
                        if text_rect.collidepoint(event.pos):
                            return seleccionar_nanograma(i, rows, cols)  

# Retorna el nanograma segun la opcion seleccionada
def seleccionar_nanograma(seleccion, rows, cols):
    if seleccion == 0:
        return (rows, cols, [[1, 1], [1, 1]], [[0, 1], [1, 0]])  # Pistas y solucion para Nanograma 1
    if seleccion == 1:
        return (rows, cols, [[2], [1]], [[1, 0], [0, 1]])  # Pistas y solucion para Nanograma 2
    if seleccion == 2:  # Opcion "Volver"
        return None  # Indica que el usuario quiere volver