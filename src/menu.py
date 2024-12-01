import pygame # type: ignore
import sys

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
COLOR_SELECC = (160, 121, 95)
COLOR_FONDO = (255, 250, 205)
COLOR_BOTON = (160, 121, 95)
COLOR_TEXTO = (50, 50, 50)


def mostrar_menu_home(screen): 

    seleccion = 0
    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption('NONOGRAMA!!') # nombre de la ventana
    font = pygame.font.SysFont('Comic Sans MS', 60) # estilo de la fuente

    # Opciones de tamaño
    opciones = ['Jugar', 'Reglas', 'Salir']

    # lista de rectángulos de posición del texto de los tamaños
    option_rects = []

    while True:
        screen.fill(COLOR_FONDO) # color del fondo 
        mouse_pos = pygame.mouse.get_pos() # posicion del mouse 
        option_rects.clear()  # Limpiar la lista en cada frame

        for i, opcion in enumerate(opciones):
            # Crear fondo para la opción seleccionada
            rect = pygame.Rect(95, 100 + i * 50, 210, 40)
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
                    if seleccion == 0:
                        return mostrar_menu_mode(screen)
                    elif seleccion == 1:
                        return mostrar_menu_reglas(screen) 
                    else:
                        pygame.quit()
                        sys.exit()

                    
            # Detectar click del mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(event.pos):
                            if i == 0:
                                return mostrar_menu_mode(screen)
                            elif i == 1:
                                return mostrar_menu_reglas(screen)
                            else:
                                pygame.quit()
                                sys.exit()


import pygame
import sys

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
COLOR_FONDO = (240, 230, 200)
COLOR_BOTON = (160, 121, 95)
COLOR_TEXTO = (50, 50, 50)

def wrap_text(text, font, max_width, margin=20):
    """
    Envuelve el texto para que se ajuste al ancho máximo de la pantalla.
    `margin` define un espacio adicional antes de alcanzar el límite máximo de la ventana.
    """
    lines = []
    words = text.split(' ')
    current_line = ""

    # Reducir el ancho máximo para dejar espacio de margen
    max_width -= margin

    for word in words:
        # Comprobar si añadir la siguiente palabra desbordaría el ancho máximo
        test_line = current_line + (word if current_line == "" else " " + word)
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    
    # Añadir la última línea
    if current_line:
        lines.append(current_line)
    
    return lines

def mostrar_menu_reglas(screen):

    pygame.display.set_caption('Reglas del Juego')  # Nombre de la ventana

    # Texto de las reglas
    reglas_text = [
        "1. Un nonograma es un rompecabezas de lógica.",
        "2. Usa las pistas para pintar celdas en el tablero.",
        "3. Las pistas indican secuencias de celdas que debes pintar.",
        "4. En el modo clásico, las celdas son blancas y negras.",
        "5. En el modo dos colores, pinta con los colores rojo y amarillo.",
        "6. No dejes espacios entre celdas pintadas de una misma pista.",
        "7. ¡Completa el tablero según las pistas para ganar!",
    ]

    # Fuentes
    font_titulo = pygame.font.SysFont('Comic Sans MS', 40)
    font_texto = pygame.font.SysFont('Comic Sans MS', 25)
    font_boton = pygame.font.SysFont('Comic Sans MS', 30)

    # Crear botón "Siguiente"
    boton_rect = pygame.Rect(
        (screen.get_width() - 200) // 2,  # Centrar el botón horizontalmente
        screen.get_height() - 70,  # Colocar el botón al final con margen
        200,  # Ancho del botón
        50  # Alto del botón
    )

    # Variable para controlar el índice de la instrucción actual
    current_instruction = 0

    while True:
        screen.fill(COLOR_FONDO)  # Fondo del tutorial

        titulo_surface = font_titulo.render("¿Cómo Jugar?", True, NEGRO)
        titulo_rect = titulo_surface.get_rect(center=(screen.get_width() // 2, 50))
        screen.blit(titulo_surface, titulo_rect)

        # Obtener el texto de la instrucción actual
        current_text = reglas_text[current_instruction]

        # Ajustar el texto para que quepa en la ventana
        max_width = screen.get_width() - 40
        lines = wrap_text(current_text, font_texto, max_width)

        # Mostrar las instrucciones ajustadas
        y_offset = 120
        for line in lines:
            texto_surface = font_texto.render(line, True, COLOR_TEXTO)
            screen.blit(texto_surface, (50, y_offset))
            y_offset += 40  # Incrementar la posición para la siguiente línea

        # Cambiar el texto del boton en la ultima pista
        if current_instruction == len(reglas_text) - 1:
            boton_text = "Jugar"
        else:
            boton_text = "Siguiente"

        # Boton Siguiente o Jugar
        pygame.draw.rect(screen, COLOR_BOTON, boton_rect, border_radius=10)
        texto_boton = font_boton.render(boton_text, True, BLANCO)
        texto_boton_rect = texto_boton.get_rect(center=boton_rect.center)
        screen.blit(texto_boton, texto_boton_rect)

        pygame.display.flip()  # Actualizar pantalla

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Cuando el usuario haga clic en el botón siguiente o jugar
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if boton_rect.collidepoint(event.pos):
                    # Si no estamos en la última instrucción, mostramos la siguiente
                    if current_instruction < len(reglas_text) - 1:
                        current_instruction += 1
                    else:
                        # Si hemos llegado al final, llamamos a la función para jugar
                        return mostrar_menu_mode(screen)

            # Usar la tecla ESC para regresar al menú principal
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return mostrar_menu_home(screen)  # Vuelve al menú de selección de modo
                elif event.key == pygame.K_RETURN:
                    if current_instruction < len(reglas_text) - 1:
                        current_instruction += 1
                    else:
                        return mostrar_menu_mode(screen)
                


def mostrar_menu_mode(screen):

    seleccion = 0
    pygame.display.set_caption('Seleccione el modo de juego') # nombre de la ventana
    font = pygame.font.SysFont('Comic Sans MS', 50) # estilo de la fuente

    # Opciones de tamaño
    opciones = ['Clásico', 'Dos colores!', 'Volver']

    # lista de rectángulos de posición del texto de los tamaños
    option_rects = []

    while True:
        screen.fill(COLOR_FONDO) # color del fondo 
        mouse_pos = pygame.mouse.get_pos() # posicion del mouse 
        option_rects.clear()  # Limpiar la lista en cada frame

        for i, opcion in enumerate(opciones):
            # Crear fondo para la opción seleccionada
            rect = pygame.Rect(90, 100 + i * 50, 220, 40)
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
                    if seleccion == 0:
                        return mostrar_menu_size(screen)
                    elif seleccion == 1:
                        return mostrar_menu_size_colores(screen)
                    else:
                        return mostrar_menu_home(screen)

                    
            # Detectar click del mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(event.pos):
                            if i == 0:
                                return mostrar_menu_size(screen)
                            elif i == 1:
                                return mostrar_menu_size_colores(screen)
                            else:
                                return mostrar_menu_home(screen)


def mostrar_menu_size(screen):

    seleccion = 0
    pygame.display.set_caption('Seleccione cual tablero quiere jugar') # nombre de la ventana
    font = pygame.font.SysFont('Comic Sans MS', 50) # estilo de la fuente

    # Opciones de tamaño
    opciones = ['5x5', '10x10', '15x15', '20x20', 'volver']

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
                pygame.draw.rect(screen, COLOR_SELECC, rect, border_radius = 10)  
                color = BLANCO  # Cambia el color del texto a blanco
            else:
                pygame.draw.rect(screen, COLOR_FONDO, rect, border_radius = 10)
                color = NEGRO

            # Renderizar el texto
            text_surface = font.render(opcion, True, color)


            #  posición del rectángulo del texto
            text_rect = text_surface.get_rect(center=(200, 120 + i * 50))  
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
                    if seleccion == 4:
                        return mostrar_menu_mode(screen)
                    else:
                        return mostrar_menu_type(screen, seleccion, "clasico")
                elif event.key == pygame.K_ESCAPE:
                    return mostrar_menu_mode(screen)

            # Detectar click del mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(event.pos):
                            if i == 4:
                                return mostrar_menu_mode(screen)
                            else:
                                return mostrar_menu_type(screen, i, "clasico")

def mostrar_menu_size_colores(screen):

    seleccion = 0
    pygame.display.set_caption('Seleccione el tamaño del tablero') # nombre de la ventana
    font = pygame.font.SysFont('Comic Sans MS', 50) # estilo de la fuente

    # Opciones de tamaño
    opciones = ['5x5', '10x10', 'volver']

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


            #  posición del rectángulo del texto
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
                    if seleccion == 2:
                        return mostrar_menu_mode(screen)
                    else:
                        return mostrar_menu_type(screen, seleccion, "dos_colores")
                elif event.key == pygame.K_ESCAPE:
                    return mostrar_menu_mode(screen)

            # Detectar click del mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(event.pos):
                            if i == 2:
                                return mostrar_menu_mode(screen)
                            else:
                                return mostrar_menu_type(screen, i, "dos_colores")

def mostrar_menu_type(screen, tamano, mode):
    seleccion = 0
    pygame.display.set_caption('Seleccione el tipo de tablero.')
    font = pygame.font.SysFont('Comic Sans MS', 50)

    if mode == "clasico":
        opciones = ['Nonograma 1', 'Nonograma 2', 'Nonograma 3', 'Volver']
    else:
        opciones = ['Nonograma 1', 'Nonograma 2', 'Volver']

    option_rects = []

    while True:
        screen.fill(COLOR_FONDO)
        mouse_pos = pygame.mouse.get_pos()
        option_rects.clear()

        for i, opcion in enumerate(opciones):
            rect = pygame.Rect(65, 100 + i * 50, 270, 40)
            if i == seleccion:
                pygame.draw.rect(screen, COLOR_SELECC, rect, border_radius=10)
                color = BLANCO
            else:
                pygame.draw.rect(screen, COLOR_FONDO, rect, border_radius=10)
                color = NEGRO

            text_surface = font.render(opcion, True, color)
            text_rect = text_surface.get_rect(center=(200, 120 + i * 50))

            option_rects.append(text_rect)

            if text_rect.collidepoint(mouse_pos):
                seleccion = i

            screen.blit(text_surface, text_rect)

        pygame.display.flip()

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
                    if seleccion == 0:
                        return nanogramas_type(tamano, 1, mode)
                    elif seleccion == 1:
                        return nanogramas_type(tamano, 2, mode)
                    elif seleccion == 2:
                        if mode != "clasico": return mostrar_menu_size_colores(screen)
                        else: return nanogramas_type(tamano, 3, mode)
                    else:
                        return mostrar_menu_size(screen)
            
                elif event.key == pygame.K_ESCAPE:
                    if mode == "clasico":
                        return mostrar_menu_size(screen)
                    else:
                        return mostrar_menu_size_colores(screen)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(event.pos):
                            if i == 0:
                                return nanogramas_type(tamano, 1, mode)
                            elif i == 1:
                                return nanogramas_type(tamano, 2, mode)
                            elif i == 2:
                                if mode != "clasico": return mostrar_menu_size_colores(screen)
                                else: return nanogramas_type(tamano, 3, mode)
                            else:
                                return mostrar_menu_size(screen)
                                


def nanogramas_type(tamano, tipo, mode):
    tamanos = {
        0: (5, 5, tipo, mode),
        1: (10, 10, tipo, mode),
        2: (15, 15, tipo, mode),
        3: (20, 20, tipo, mode),
    }
    return tamanos.get(tamano)
