import pygame

pygame.init()

#Configuración del ícono y el nombre de la ventana
pygame.display.set_caption("F1 Simulation")
ICONO = pygame.image.load('C:/Users/joaco/OneDrive/Desktop/UDESA/primer AÑO 1er CUATRI/Pensamiento Computacional/TPS/TPF/fotos/f1 logo.png')
pygame.display.set_icon(ICONO)

#Configuración de la pantalla
PANTALLA = pygame.display.set_mode((1000, 800)) #(ancho, alto)
FOTO_FONDO_MENU = pygame.image.load('C:/Users/joaco/OneDrive/Desktop/UDESA/primer AÑO 1er CUATRI/Pensamiento Computacional/TPS/TPF/fotos/foto fondo menu.png')
COLOR_DE_FONDO = (34, 139, 34)

#Jugadores: configuración inicial
JUGADOR_IMG_1 = pygame.image.load('C:/Users/joaco/OneDrive/Desktop/UDESA/primer AÑO 1er CUATRI/Pensamiento Computacional/TPS/TPF/fotos/auto 1.png')
JUGADOR_IMG_2 = pygame.image.load('C:/Users/joaco/OneDrive/Desktop/UDESA/primer AÑO 1er CUATRI/Pensamiento Computacional/TPS/TPF/fotos/auto 2.png')
jugador_1_pos = [-100, 300]
jugador_2_pos = [-70, 300]
velocidad_1 = [0, 0]
velocidad_2 = [0, 0]

#Función para mostrar a los jugadores
def mostrar_jugador(imagen, posicion):
    """Dibuja un jugador en la pantalla en la posición dada."""
    PANTALLA.blit(imagen, (posicion[0], posicion[1]))

#Función para manejar el menú
def mostrar_menu():
    """Muestra el menú inicial y devuelve la selección del modo de juego."""
    seleccion = None
    while seleccion is None:
        PANTALLA.blit(FOTO_FONDO_MENU, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    seleccion = 1
                elif event.key == pygame.K_2:
                    seleccion = 2

        pygame.display.update()
    return seleccion

#Función para manejar el movimiento
def actualizar_posicion(posicion, velocidad):
    """Actualiza la posición de un jugador según su velocidad."""
    posicion[0] += velocidad[0]
    posicion[1] += velocidad[1]

#Función para manejar los controles
def manejar_controles(event, modo_de_juego, velocidad_1, velocidad_2):
    """Gestiona los eventos de teclado y actualiza las velocidades."""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
            velocidad_1[1] = -2
        elif event.key == pygame.K_s:
            velocidad_1[1] = 2
        elif event.key == pygame.K_a:
            velocidad_1[0] = -2
        elif event.key == pygame.K_d:
            velocidad_1[0] = 2

        if modo_de_juego == 2:
            if event.key == pygame.K_UP:
                velocidad_2[1] = -2
            elif event.key == pygame.K_DOWN:
                velocidad_2[1] = 2
            elif event.key == pygame.K_LEFT:
                velocidad_2[0] = -2
            elif event.key == pygame.K_RIGHT:
                velocidad_2[0] = 2

    if event.type == pygame.KEYUP:
        if event.key in (pygame.K_w, pygame.K_s):
            velocidad_1[1] = 0
        if event.key in (pygame.K_a, pygame.K_d):
            velocidad_1[0] = 0

        if modo_de_juego == 2:
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                velocidad_2[1] = 0
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                velocidad_2[0] = 0

#Modo de juego
modo_de_juego = mostrar_menu()

#Loop principal
running = True
while running:
    PANTALLA.fill(COLOR_DE_FONDO)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            jugador_1_pos = [-100, 300]
            jugador_2_pos = [-70, 300]
            modo_de_juego = mostrar_menu()

        manejar_controles(event, modo_de_juego, velocidad_1, velocidad_2)

    #Actualizar posiciones
    actualizar_posicion(jugador_1_pos, velocidad_1)
    if modo_de_juego == 2:
        actualizar_posicion(jugador_2_pos, velocidad_2)

    #Dibujar jugadores
    mostrar_jugador(JUGADOR_IMG_1, jugador_1_pos)
    if modo_de_juego == 2:
        mostrar_jugador(JUGADOR_IMG_2, jugador_2_pos)

    pygame.display.update()

pygame.quit()
