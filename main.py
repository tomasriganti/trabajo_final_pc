import pygame
from track.track import Track
from car.player_car import PlayerCar
from car.auto_car import AutoCar
import time

# Inicialización de Pygame
pygame.init()

# Configuración del ícono y el nombre de la ventana
pygame.display.set_caption("F1 Simulation")
ICONO = pygame.image.load('C:/Users/joaco/OneDrive/Desktop/UDESA/primer AÑO 1er CUATRI/Pensamiento Computacional/TPS/TPF/fotos/f1 logo.png')
pygame.display.set_icon(ICONO)

# Configuración de la pantalla
PANTALLA = pygame.display.set_mode((1000, 800))  # (ancho, alto)
FOTO_FONDO_MENU = pygame.image.load('C:/Users/joaco/OneDrive/Desktop/UDESA/primer AÑO 1er CUATRI/Pensamiento Computacional/TPS/TPF/fotos/foto menu.png')
COLOR_DE_FONDO = (34, 139, 34)

# Fuentes para texto
fuente = pygame.font.Font(None, 36)  # Fuente para el contador de vueltas
fuente_ganador = pygame.font.Font(None, 72)  # Fuente para el mensaje de ganador

# Crear la pista
pista = Track(x_max=1000, y_max=800, width=65)

# Obtener posición y dirección inicial
posicion_inicial = pista.get_starting_position()
direccion_inicial = pista.get_starting_direction()

# JUGADOR 1
FOTO_JUGADOR_1 = pygame.image.load("C:/Users/joaco/OneDrive/Desktop/UDESA/primer AÑO 1er CUATRI/Pensamiento Computacional/TPS/TPF/fotos/Auto 1.png")
controles_Jugador_1 = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
Jugador_1_clase = PlayerCar("Colapinto", 43, controles_Jugador_1)
Jugador_1_clase.set_position(posicion_inicial)
Jugador_1_clase.set_direction(direccion_inicial)
vueltas_jugador_1 = 0
trayectoria_jugador_1 = [posicion_inicial]

# JUGADOR 2
FOTO_JUGADOR_2 = pygame.image.load("C:/Users/joaco/OneDrive/Desktop/UDESA/primer AÑO 1er CUATRI/Pensamiento Computacional/TPS/TPF/fotos/Auto 2.png")
controles_Jugador_2 = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
Jugador_2_clase = PlayerCar("Sainz", 55, controles_Jugador_2)
Jugador_2_clase.set_position([posicion_inicial[0] + 10, posicion_inicial[1] + 10]) 
Jugador_2_clase.set_direction(direccion_inicial)
vueltas_jugador_2 = 0
trayectoria_jugador_2 = [Jugador_2_clase.get_position()]

# CPU
Auto_CPU = AutoCar("Perez", 11)
Auto_CPU.set_position([posicion_inicial[0] - 10, posicion_inicial[1] - 10]) 
Auto_CPU.set_direction(direccion_inicial)
vueltas_jugador_CPU = 0
trayectoria_cpu = [Auto_CPU.get_position()]

# Variables del tiempo
tiempo_inicio = time.time()
tiempo_vuelta = 0

run = True
clock = pygame.time.Clock()
TICK_POR_TIEMPO = 100
ganador = None 

while run:
    PANTALLA.fill(COLOR_DE_FONDO)
    clock.tick(TICK_POR_TIEMPO)
    keys = pygame.key.get_pressed()

    # Dibujar la pista
    if pista.track_polygon:
        pygame.draw.polygon(PANTALLA, (128, 128, 128), list(pista.track_polygon.exterior.coords), 0)
        for hole in pista.track_polygon.interiors:
            pygame.draw.polygon(PANTALLA, COLOR_DE_FONDO, list(hole.coords), 0)

    # Dibujar línea de meta
    pygame.draw.line(PANTALLA, (255, 255, 255), (int(pista.finish_line.coords[0][0]), int(pista.finish_line.coords[0][1])), (int(pista.finish_line.coords[1][0]), int(pista.finish_line.coords[1][1])), 5)

    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    # Verificar y reducir velocidad si los jugadores están fuera de la pista
    if not pista.is_point_inside_track(Jugador_1_clase.get_position()):
        Jugador_1_clase.set_speed(Jugador_1_clase.get_speed() / 10)

    if not pista.is_point_inside_track(Jugador_2_clase.get_position()):
        Jugador_2_clase.set_speed(Jugador_2_clase.get_speed() / 10)

    # Mover y dibujar jugador 1 (círculo azul)
    trayectoria_jugador_1.append(Jugador_1_clase.get_position())
    if pista.check_lap([trayectoria_jugador_1[-2], trayectoria_jugador_1[-1]]):
        vueltas_jugador_1 += 1
    Jugador_1_clase.move_car(keys)
    pygame.draw.circle(PANTALLA, (0, 0, 255), (int(Jugador_1_clase.x), int(Jugador_1_clase.y)), 10)

    # Mover y dibujar jugador 2 (círculo rojo)
    trayectoria_jugador_2.append(Jugador_2_clase.get_position())
    if pista.check_lap([trayectoria_jugador_2[-2], trayectoria_jugador_2[-1]]):
        vueltas_jugador_2 += 1
    Jugador_2_clase.move_car(keys)
    pygame.draw.circle(PANTALLA, (255, 0, 0), (int(Jugador_2_clase.x), int(Jugador_2_clase.y)), 10)

    # Verificar ganador
    if vueltas_jugador_1 >= 3:
        ganador = f'{Jugador_1_clase.driver_name}'
        run = False
    elif vueltas_jugador_2 >= 3:
        ganador = f'{Jugador_2_clase.driver_name}'
        run = False

    # Mostrar el contador de vueltas en la pantalla
    texto_vueltas = fuente.render(f"Jugador 1: {vueltas_jugador_1} vueltas | Jugador 2: {vueltas_jugador_2} vueltas", True, (255, 255, 255))
    PANTALLA.blit(texto_vueltas, (10, 10))
    
    # Actualizar pantalla
    pygame.display.update()

# Mostrar mensaje del ganador
if ganador:
    mensaje_ganador = fuente_ganador.render(f"¡{ganador} gana!", True, (255, 255, 0))
    PANTALLA.fill(COLOR_DE_FONDO)
    PANTALLA.blit(mensaje_ganador, (PANTALLA.get_width() // 2 - mensaje_ganador.get_width() // 2, PANTALLA.get_height() // 2 - mensaje_ganador.get_height() // 2))
    pygame.display.update()
    time.sleep(5)  # Mostrar el mensaje durante 5 segundos

pygame.quit()
