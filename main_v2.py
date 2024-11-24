import pygame
import random
from shapely.geometry import Point
from track.track import Track
import time  # Para medir el tiempo de la vuelta

pygame.init()

# Configuración del ícono y el nombre de la ventana
pygame.display.set_caption("F1 Simulation")
ICONO = pygame.image.load('fotos/f1 logo.png')
pygame.display.set_icon(ICONO)

# Crear la pista
pista = Track(x_max=1000, y_max=800, width=50)

# Configuración de la pantalla
PANTALLA = pygame.display.set_mode((1000, 800))  # (ancho, alto)
FOTO_FONDO_MENU = pygame.image.load('fotos/foto fondo menu.png')
COLOR_DE_FONDO = (34, 139, 34)

# Jugadores: configuración inicial
JUGADOR_IMG_1 = pygame.image.load('fotos/auto 1.png')
JUGADOR_IMG_2 = pygame.image.load('fotos/auto 2.png')

# Obtener una posición inicial aleatoria dentro de la pista
def obtener_posicion_inicial_aleatoria(track_polygon):
    while True:
        x = random.randint(0, 1000)
        y = random.randint(0, 800)
        if track_polygon.contains(Point(x, y)):
            return [x, y]

# Establecer la posición inicial y la línea de meta
jugador_1_pos = obtener_posicion_inicial_aleatoria(pista.track_polygon)
jugador_2_pos = [jugador_1_pos[0] + 50, jugador_1_pos[1] + 50]

velocidad_1 = [0, 0]
velocidad_2 = [0, 0]
ultima_posicion_jugador_1 = list(jugador_1_pos)
ultima_posicion_jugador_2 = list(jugador_2_pos)

# Función para mostrar a los jugadores
def mostrar_jugador(imagen, posicion):
    """Dibuja un jugador en la pantalla en la posición dada."""
    PANTALLA.blit(imagen, (posicion[0], posicion[1]))

# Función para manejar el menú
def mostrar_menu():
    """Muestra el menú inicial y devuelve la selección del modo de juego."""
    seleccion = None
    font = pygame.font.Font(None, 36)  # Fuente para el texto

    while seleccion is None:
        PANTALLA.blit(FOTO_FONDO_MENU, (0, 0))

        # Texto de instrucciones
        texto_1 = font.render("Presione 1 para un jugador", True, (255, 255, 255))
        texto_2 = font.render("Presione 2 para dos jugadores", True, (255, 255, 255))
        
        # Centrar el texto en la parte inferior
        texto_1_rect = texto_1.get_rect(center=(500, 650))
        texto_2_rect = texto_2.get_rect(center=(500, 700))
        
        # Mostrar el texto en la pantalla
        PANTALLA.blit(texto_1, texto_1_rect)
        PANTALLA.blit(texto_2, texto_2_rect)

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

# Función para manejar el movimiento
def actualizar_posicion(posicion, velocidad, pista):
    """
    Actualiza la posición de un jugador según su velocidad.
    Si está fuera de la pista, la velocidad se reduce a una décima parte.
    """
    """
    if pista.track_polygon.contains(Point(posicion[0], posicion[1])): descomentar cuando se solucione que el auto spawnee en pista y no en cualq lugar
        posicion[0] += velocidad[0]
        posicion[1] += velocidad[1]
    else:
        velocidad[0] *= 0.1
        velocidad[1] *= 0.1
        posicion[0] += velocidad[0]
        posicion[1] += velocidad[1]
    """
    posicion[0] += velocidad[0]
    posicion[1] += velocidad[1]

# Función para manejar los controles
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

# Modo de juego
modo_de_juego = mostrar_menu()

# Variables para las vueltas y el tiempo
vueltas = 1  # Iniciar el contador de vueltas en 1
tiempo_inicio = time.time()  # Empezar el cronómetro al comenzar la vuelta
tiempo_vuelta = 0

# Loop principal
running = True
while running:
    # Dibujar fondo
    PANTALLA.fill(COLOR_DE_FONDO)

    # Dibujar la pista
    if pista.track_polygon:
        pygame.draw.polygon(PANTALLA, (128, 128, 128), list(pista.track_polygon.exterior.coords), 0)
        for hole in pista.track_polygon.interiors:
            pygame.draw.polygon(PANTALLA, COLOR_DE_FONDO, list(hole.coords), 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            jugador_1_pos = obtener_posicion_inicial_aleatoria(pista.track_polygon)
            jugador_2_pos = [jugador_1_pos[0] + 50, jugador_1_pos[1] + 50]
            modo_de_juego = mostrar_menu()

        manejar_controles(event, modo_de_juego, velocidad_1, velocidad_2)

    # Actualizar posiciones
    actualizar_posicion(jugador_1_pos, velocidad_1, pista)
    if modo_de_juego == 2:
        actualizar_posicion(jugador_2_pos, velocidad_2, pista)

    # Dibujar jugadores
    mostrar_jugador(JUGADOR_IMG_1, jugador_1_pos)
    if modo_de_juego == 2:
        mostrar_jugador(JUGADOR_IMG_2, jugador_2_pos)

    pygame.display.update()

pygame.quit()
