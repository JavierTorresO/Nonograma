import pygame # type: ignore
import sys

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
COLOR_SELECC = (160, 121, 95)
COLOR_FONDO = (255, 250, 205)
pantalla = None


def mostrar_menu_size(screen):
    global pantalla
    pantalla = screen
    seleccion = 0
    tipo=0
    pygame.display.set_caption('Seleccione el tablero.')

    font = pygame.font.SysFont('Comic Sans MS', 40)

    # Opciones de tamaño
    opciones = ['5x5', '10x10', '15x15', '20x20', 'Salir']

    # lista de rectángulos de posición del texto de los tamaños
    option_rects = []

    while True:
        screen.fill(COLOR_FONDO)

        # posicion del mouse
        mouse_pos = pygame.mouse.get_pos()

        option_rects.clear()  # Limpiar la lista en cada frame
        for i, opcion in enumerate(opciones):
            # Crear fondo para la opción seleccionada
            rect = pygame.Rect(100, 100 + i * 50, 200, 40)
            if i == seleccion:
                pygame.draw.rect(screen, COLOR_SELECC, rect, border_radius = 10)  # Fondo rojo para opción seleccionada
                color = BLANCO  # Cambia el color del texto a blanco
            else:
                pygame.draw.rect(screen, COLOR_FONDO, rect, border_radius = 10)
                color = NEGRO

            # Renderizar el texto
            text_surface = font.render(opcion, True, color)


            # Obtener la posición del rectángulo del texto
            text_rect = text_surface.get_rect(center=(200, 120 + i * 50))  # centrado en el eje X
            option_rects.append(text_rect)

            # Resaltar la opción con el mouse
            if text_rect.collidepoint(mouse_pos):
                seleccion = i  # Cambia la opción seleccionada al pasar el mouse

            screen.blit(text_surface, text_rect)

        pygame.display.flip()

        # Manejar eventos
        for event in pygame.event.get():
            # Salir al apretar boton de cierre
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Para funcionar con las flechas, enter y escape
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif event.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif event.key == pygame.K_RETURN:
                    return seleccionar_opcion(seleccion)

            # Detectar click del mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(event.pos):
                            return seleccionar_opcion(i)


def mostrar_menu_type(screen):
    tipo = 0
    pygame.display.set_caption('Seleccione el tipo de tablero.')
    font = pygame.font.SysFont('Comic Sans MS', 40)

    # Opciones de tipo
    opciones = ['Nanograma 1', 'Nanograma 2', 'Volver']
    option_rects = []

    while True:
        screen.fill(COLOR_FONDO)

        # posicion del mouse
        mouse_pos = pygame.mouse.get_pos()

        option_rects.clear()  # Limpiar la lista en cada frame
        for i, opcion in enumerate(opciones):
            rect = pygame.Rect(100, 100 + i * 50, 200, 40)
            # Crear fondo para la opción seleccionada
            if i == tipo:
                pygame.draw.rect(screen, COLOR_SELECC, rect, border_radius = 10)  # Fondo COLOR_SELECC para opción seleccionada
                color = BLANCO  # Cambia el color del texto a blanco
            else:
                pygame.draw.rect(screen, COLOR_FONDO, rect, border_radius = 10)
                color = NEGRO

            # Renderizar el texto
            text_surface = font.render(opcion, True, color)

            # Obtener la posición del rectángulo del texto
            text_rect = text_surface.get_rect(center=(200, 120 + i * 50))  # Centrado en el eje X
            option_rects.append(text_rect)

            # Resaltar la opción con el mouse
            if text_rect.collidepoint(mouse_pos):
                tipo = i  # Cambia la opción seleccionada al pasar el mouse

            screen.blit(text_surface, text_rect)

        pygame.display.flip()
        # Manejar eventos
        for event in pygame.event.get():
            # Salir al apretar boton de cierre
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # # Para funcionar con las flechas, enter y escape
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    tipo = (tipo + 1) % len(opciones)
                elif event.key == pygame.K_UP:
                    tipo = (tipo - 1) % len(opciones)
                elif event.key == pygame.K_RETURN:
                    if tipo == 0:
                        return 1
                    elif tipo == 1:
                        return 2
                    else:
                        mostrar_menu_size(screen)
                elif event.key == pygame.K_ESCAPE:
                    mostrar_menu_size(screen)

            # Detectar click del mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(event.pos):
                            if i == 0:
                                return 1
                            elif i == 1:
                                return 2
                            else:
                                mostrar_menu_size(screen)


# Retorna el tamaño del tablero segun la opcion seleccionada
def seleccionar_opcion(seleccion):
    global pantalla
    
    if seleccion == 4:
        pygame.quit()
        sys.exit()
    
    tipo = mostrar_menu_type(pantalla)
    
    tamano = {
        0: (5, 5, tipo),
        1: (10, 10, tipo),
        2: (15, 15, tipo),
        3: (20, 20, tipo),
    }
    
    return (tamano.get(seleccion))