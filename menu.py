import pygame # type: ignore
import sys

#colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

def mostrar_menu(screen):
    pygame.display.set_caption('Seleccione el tablero.')

    font = pygame.font.SysFont('Comic Sans MS', 30)

    #opciones de tamano
    opciones = ['5x5', '10x10', '15x15', '20x20', 'Salir']
    seleccion = 0
    
    while True:
        screen.fill(BLANCO)

        for i, opcion in enumerate (opciones):
            if i == seleccion:
                color = (255, 0, 0) #Color rojo para la opcion seleccionada
            else:
                color = NEGRO
            
            text_surface = font.render(opcion, True, color)
            screen.blit(text_surface, (100, 100+i * 50))

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
                        return(5,5)
                    if seleccion == 1:
                        return(10,10) 
                    if seleccion == 2:
                        return(15,15)
                    if seleccion == 3:
                        return(20,20)
                    if seleccion == 4:
                        pygame.quit()
                        sys.exit()

#Ejemplo de como se podria llamar


