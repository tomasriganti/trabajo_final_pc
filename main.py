import pygame
from track.track import Track
from car.player_car import PlayerCar
from car.auto_car import AutoCar
import math
from funciones_TPF import mostrar_menu, mostrar_contador, reproducir_sonido, mensaje_ganador

pygame.init()

#Configuración del ícono y el nombre de la ventana
pygame.display.set_caption("F1 Simulation")
ICONO = pygame.image.load('fotos/f1 logo.png')
pygame.display.set_icon(ICONO)

#Configuración de la pantalla
PANTALLA = pygame.display.set_mode((1000, 800))  # (ancho, alto)
FOTO_FONDO_MENU = pygame.image.load('fotos/Foto menu.png')
COLOR_DE_FONDO = (34, 139, 34)
AMARILLO = (238, 202, 6)

#sonidos
SONIDO_AUTO_F1 = 'sonidos/sonido de auto f1.mp3'
SONIDO_MUSICA_FONDO = 'sonidos/musica fondo juego.mp3'
SONIDO_VICTORIA = 'sonidos/sonido victoria.mp3'

# Música de fondo
pygame.mixer.music.load(SONIDO_MUSICA_FONDO)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5) 

#Fuentes para texto
fuente_1 = pygame.font.Font(None, 36) 
fuente_ganador = pygame.font.Font(None, 72) 

clock = pygame.time.Clock()
TICK_POR_TIEMPO = 100
ganador = None

# Crear la pista
pista = Track(num_points=10, x_max=1000, y_max=800, width=70)

# Obtener posición y dirección inicial
posicion_inicial = pista.get_starting_position()
direccion_inicial = pista.get_starting_direction()

# JUGADOR 1
FOTO_ORIGINAL_1 = pygame.image.load("fotos/auto Colapinto.png")
FOTO_JUGADOR_1 = pygame.image.load("fotos/auto Colapinto.png")
controles_Jugador_1 = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
Jugador_1 = PlayerCar("Colapinto", 43, controles_Jugador_1)
Jugador_1.set_position(posicion_inicial)
Jugador_1.set_direction(direccion_inicial)
vueltas_jugador_1 = 0
trayectoria_jugador_1 = [Jugador_1.get_position()]


# JUGADOR 2
FOTO_ORIGINAL_2 = pygame.image.load("fotos/auto Sainz.png")
FOTO_JUGADOR_2 = pygame.image.load("fotos/auto Sainz.png")
controles_Jugador_2 = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
Jugador_2 = PlayerCar("Sainz", 55, controles_Jugador_2)
Jugador_2.set_position([posicion_inicial[0], posicion_inicial[1]])
Jugador_2.set_direction(direccion_inicial)
vueltas_jugador_2 = 0
trayectoria_jugador_2 = [Jugador_2.get_position()]


#JUGADOR CPU
FOTO_CPU_ORIGINAL = pygame.image.load("fotos/auto Perez.png")
FOTO_CPU = pygame.image.load("fotos/auto Perez.png")
Jugador_CPU = AutoCar("Perez", 11)
Jugador_CPU.set_position([posicion_inicial[0], posicion_inicial[1]])
Jugador_CPU.set_direction(direccion_inicial)
vueltas_jugador_CPU = 0
trayectoria_cpu = [Jugador_CPU.get_position()]

# Inicialización del menú principal
modo_juego = mostrar_menu(PANTALLA, FOTO_FONDO_MENU, fuente_1)

# Mostrar el contador antes de iniciar la carrera
mostrar_contador(PANTALLA, fuente_ganador, AMARILLO, 3, COLOR_DE_FONDO)


# bucle principal
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    PANTALLA.fill(COLOR_DE_FONDO)
    clock.tick(TICK_POR_TIEMPO)
    keys = pygame.key.get_pressed()

    # Dibujar la pista
    if pista.track_polygon:
        pygame.draw.polygon(PANTALLA, AMARILLO, list(pista.track_polygon.exterior.coords), width=5)
        pygame.draw.polygon(PANTALLA, (128, 128, 128), list(pista.track_polygon.exterior.coords), 0)
        for hole in pista.track_polygon.interiors:
            pygame.draw.polygon(PANTALLA, AMARILLO, list(hole.coords), width=5)
            pygame.draw.polygon(PANTALLA, COLOR_DE_FONDO, list(hole.coords), 0)
    #linea meta
    pygame.draw.lines(PANTALLA, (255, 255, 255), False, pista.finish_line.coords, 5)

    if modo_juego == 1:
        # Mover y dibujar Jugador_1
        FOTO_JUGADOR_1 = pygame.transform.rotate(FOTO_ORIGINAL_1, math.degrees(-Jugador_1.get_direction()))
        PANTALLA.blit(FOTO_JUGADOR_1, (int(Jugador_1.get_position()[0])-18, int(Jugador_1.get_position()[1])-18))
        trayectoria_jugador_1.append(Jugador_1.get_position())
        if pista.check_lap([trayectoria_jugador_1[-2], trayectoria_jugador_1[-1]]):
            vueltas_jugador_1 += 1
            reproducir_sonido(SONIDO_AUTO_F1)
        J1_inside = pista.is_point_inside_track(Jugador_1.get_position())
        J1_commands = Jugador_1.get_command(keys, J1_inside)
        Jugador_1.send_command(J1_commands[0], J1_commands[1])
        pista.move_car(Jugador_1)

        # CPU
        FOTO_CPU = pygame.transform.rotate(FOTO_CPU_ORIGINAL, math.degrees(-Jugador_CPU.get_direction()))
        PANTALLA.blit(FOTO_CPU, (int(Jugador_CPU.get_position()[0])-18, int(Jugador_CPU.get_position()[1])-18))
        trayectoria_cpu.append(Jugador_CPU.get_position())
        if pista.check_lap([trayectoria_cpu[-2], trayectoria_cpu[-1]]):
            vueltas_jugador_CPU += 1
            reproducir_sonido(SONIDO_AUTO_F1)
        CPU_inside = pista.is_point_inside_track(Jugador_CPU.get_position())
        CPU_commands = Jugador_CPU.get_command(pista.get_distances_car(Jugador_CPU.get_position(), Jugador_CPU.get_direction()), CPU_inside)
        Jugador_CPU.send_command(CPU_commands[0], CPU_commands[1])
        pista.move_car(Jugador_CPU)

    elif modo_juego == 2:
        # Mover y dibujar Jugador_1
        FOTO_JUGADOR_1 = pygame.transform.rotate(FOTO_ORIGINAL_1, math.degrees(-Jugador_1.get_direction()))
        PANTALLA.blit(FOTO_JUGADOR_1, (int(Jugador_1.get_position()[0])-18, int(Jugador_1.get_position()[1])-18))
        trayectoria_jugador_1.append(Jugador_1.get_position())
        if pista.check_lap([trayectoria_jugador_1[-2], trayectoria_jugador_1[-1]]):
            vueltas_jugador_1 += 1
            reproducir_sonido(SONIDO_AUTO_F1)
        J1_inside = pista.is_point_inside_track(Jugador_1.get_position())
        J1_commands = Jugador_1.get_command(keys, J1_inside)
        Jugador_1.send_command(J1_commands[0], J1_commands[1])
        pista.move_car(Jugador_1)

        # Mover y dibujar Jugador_2
        FOTO_JUGADOR_2 = pygame.transform.rotate(FOTO_ORIGINAL_2, math.degrees(-Jugador_2.get_direction()))
        PANTALLA.blit(FOTO_JUGADOR_2, (int(Jugador_2.get_position()[0])-18, int(Jugador_2.get_position()[1])-18))
        trayectoria_jugador_2.append(Jugador_2.get_position())
        if pista.check_lap([trayectoria_jugador_2[-2], trayectoria_jugador_2[-1]]):
            vueltas_jugador_2 += 1
            reproducir_sonido(SONIDO_AUTO_F1)
        J2_inside = pista.is_point_inside_track(Jugador_2.get_position())
        J2_commands = Jugador_2.get_command(keys, J2_inside)
        Jugador_2.send_command(J2_commands[0], J2_commands[1])
        pista.move_car(Jugador_2)

        # CPU
        FOTO_CPU = pygame.transform.rotate(FOTO_CPU_ORIGINAL, math.degrees(-Jugador_CPU.get_direction()))
        PANTALLA.blit(FOTO_CPU, (int(Jugador_CPU.get_position()[0])-18, int(Jugador_CPU.get_position()[1])-18))
        trayectoria_cpu.append(Jugador_CPU.get_position())
        if pista.check_lap([trayectoria_cpu[-2], trayectoria_cpu[-1]]):
            vueltas_jugador_CPU += 1
            reproducir_sonido(SONIDO_AUTO_F1)
        CPU_inside = pista.is_point_inside_track(Jugador_CPU.get_position())
        CPU_commands = Jugador_CPU.get_command(pista.get_distances_car(Jugador_CPU.get_position(), Jugador_CPU.get_direction()), CPU_inside)
        Jugador_CPU.send_command(CPU_commands[0], CPU_commands[1])
        pista.move_car(Jugador_CPU)

    # Mostrar contador de vueltas
    texto_vueltas = fuente_1.render(
        f"{Jugador_1.driver_name}: {vueltas_jugador_1}/3 vueltas | {Jugador_2.driver_name}: {vueltas_jugador_2}/3 vueltas | {Jugador_CPU.driver_name}: {vueltas_jugador_CPU}/3 vueltas", 
        True, 
        AMARILLO
    )
    PANTALLA.blit(texto_vueltas, (10, 10))

    # Verificar ganador
    if vueltas_jugador_1 >= 3:
        ganador = f'{Jugador_1.driver_name}'
        run = False
    elif vueltas_jugador_2 >= 3:
        ganador = f'{Jugador_2.driver_name}'
        run = False
    elif vueltas_jugador_CPU >= 3:
        ganador = f'{Jugador_CPU.driver_name}'
        run = False

    # Actualizar pantalla
    pygame.display.update()


pygame.mixer.music.stop() 
# Mostrar mensaje del ganador
mensaje_ganador(ganador, PANTALLA, COLOR_DE_FONDO, fuente_ganador, AMARILLO, SONIDO_VICTORIA)

pygame.quit()
