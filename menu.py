import pygame # type: ignore
import sys

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
pantalla = None

def mostrar_menu_size(screen):
    global pantalla
    pantalla = screen
    seleccion = 0
    pygame.display.set_caption('Seleccione el tablero.')

    font = pygame.font.SysFont('Comic Sans MS', 30)

    # Opciones de tamaño
    opciones = ['5x5', '10x10', '15x15', '20x20', 'Salir']
    
    # lista de rectangulos de posicion del texto de los tamañaos
    option_rects = []

    while True:
        screen.fill(BLANCO)

        # posicion del mouse
        mouse_pos = pygame.mouse.get_pos()

        option_rects.clear()  # Limpiar la lista en cada frame
        for i, opcion in enumerate(opciones):
            if i == seleccion:
                color = ROJO  # Color rojo para la opcion seleccionada con las teclas
            else:
                color = NEGRO

            # Renderizar el texto
            text_surface = font.render(opcion, True, color)

            # Obtener la posicion del rectangulo del texto 
            text_rect = text_surface.get_rect(topleft=(100, 100 + i * 50))
            option_rects.append(text_rect)

            if text_rect.collidepoint(mouse_pos):
                text_surface = font.render(opcion, True, ROJO)  # Color rojo si el mouse está sobre la opcion
                seleccion = i 

            screen.blit(text_surface, text_rect)

        pygame.display.flip()

        # Manejar eventos
        for event in pygame.event.get():
            # Salir al apretar boton de cierre
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Movimiento de las teclas
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


# Muestra el menu de seleccion de tipo de tablero
def mostrar_menu_type(screen):
    tipo = 0
    pygame.display.set_caption('Seleccione el tipo de tablero.')
    font = pygame.font.SysFont('Comic Sans MS', 30)

    # Opciones de tipo
    opciones = ['Nanograma 1', 'Nanograma 2', 'Volver']
    option_rects = []
    
    while True:
        screen.fill(BLANCO)

        # posicion del mouse
        mouse_pos = pygame.mouse.get_pos()

        option_rects.clear()  # Limpiar la lista en cada frame
        for i, opcion in enumerate(opciones):
            if i == tipo:
                color = ROJO  # Color rojo para la opcion seleccionada con las teclas
            else:
                color = NEGRO

            # Renderizar el texto
            text_surface = font.render(opcion, True, color)

            # Obtener la posicion del rectangulo del texto 
            text_rect = text_surface.get_rect(topleft=(100, 100 + i * 50))
            option_rects.append(text_rect)

            if text_rect.collidepoint(mouse_pos):
                text_surface = font.render(opcion, True, ROJO)  # Color rojo si el mouse está sobre la opcion
                tipo = i 

            screen.blit(text_surface, text_rect)

        pygame.display.flip()
         # Manejar eventos
        for event in pygame.event.get():
            # Salir al apretar boton de cierre
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Movimiento de las teclas
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