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
    pygame.display.set_caption('Seleccione el tablero.') # nombre de la ventana
    font = pygame.font.SysFont('Comic Sans MS', 40) # estilo de la fuente

    # Opciones de tamaño
    opciones = ['5x5', '10x10', '15x15', '20x20', 'Salir']

    # lista de rectángulos de posición del texto de los tamaños
    option_rects = []

    while True:
        screen.fill(COLOR_FONDO) # color del fondo 
        mouse_pos = pygame.mouse.get_pos() # posicion del mouse 
        option_rects.clear()  # Limpiar la lista en cada frame

        for i, opcion in enumerate(opciones):
            # Crear fondo para la opción seleccionada
            rect = pygame.Rect(100, 100 + i * 50, 200, 40)
            if i == seleccion:
                pygame.draw.rect(screen, COLOR_SELECC, rect, border_radius = 10)  # Fondo color para opción seleccionada
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

            screen.blit(text_surface, text_rect) # renderiza el texto

        pygame.display.flip() # actiualiza la pantalla para mostrar los cambios en este frame

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
    pygame.display.set_caption('Seleccione el tipo de tablero.') # Nombre de la ventana
    font = pygame.font.SysFont('Comic Sans MS', 40) # Estilo de la fuente

    # Opciones de tipo
    opciones = ['Nanograma 1', 'Nanograma 2', 'Nanograma 3', 'Volver']
    option_rects = []

    while True:
        screen.fill(COLOR_FONDO) # Color del fondo
        mouse_pos = pygame.mouse.get_pos() # posicion del mouse
        option_rects.clear()  # Limpiar la lista en cada frame

        for i, opcion in enumerate(opciones):
            rect = pygame.Rect(65, 105 + i * 50, 270, 40)
            
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

            screen.blit(text_surface, text_rect) # renderizar

        pygame.display.flip() # actualizar
        # Manejar eventos
        for event in pygame.event.get():
            # Salir al apretar boton de cierre
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # # Para funcionar con las flechas, enter y escape
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:  # Mover hacia abajo
                    tipo = (tipo + 1) % len(opciones)
                elif event.key == pygame.K_UP:  # Mover hacia arriba
                    tipo = (tipo - 1) % len(opciones)
                elif event.key == pygame.K_RETURN:  # Confirmar selección
                    if tipo in [0, 1, 2]:  # Seleccionar un nonograma
                        return tipo + 1
                    elif tipo == 3:  # Volver
                        return None
                elif event.key == pygame.K_ESCAPE:  # Volver con ESC
                    return None

            # Detectar click del mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(event.pos):
                            if i in [0, 1, 2]:
                                return i + 1
                            elif i == 3:
                                return None


# Retorna el tamaño del tablero segun la opcion seleccionada
def seleccionar_opcion(seleccion):
    global pantalla
    
    if seleccion == 4:
        pygame.quit()
        sys.exit()
    
    tipo = mostrar_menu_type(pantalla)
    if tipo is None:  # Volver al menú principal si se selecciona "Volver"
        mostrar_menu_size(pantalla)
        return
    tamano = {
        0: (5, 5, tipo),
        1: (10, 10, tipo),
        2: (15, 15, tipo),
        3: (20, 20, tipo),
    }
    
    return (tamano.get(seleccion))