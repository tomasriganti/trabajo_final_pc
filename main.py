import pygame
from shapely.geometry import Point
from track.track import Track
from car.player_car import PlayerCar
from car.auto_car import AutoCar
import math

pygame.init()

font = pygame.font.Font(None, 36)
font_ganador = pygame.font.Font(None, 72) 

ganador = None

#Configuración de la pantalla
PANTALLA = pygame.display.set_mode((1000, 800)) #(ancho, alto)

#Nombre de ventana, fotos y colores
pygame.display.set_caption("F1 Simulation")
ICONO = pygame.image.load('C:/Users/joaco/OneDrive/Desktop/UDESA/primer AÑO 1er CUATRI/Pensamiento Computacional/TPS/TPF/fotos/f1 logo.png')
pygame.display.set_icon(ICONO)
FOTO_FONDO_MENU = pygame.image.load('C:/Users/joaco/OneDrive/Desktop/UDESA/primer AÑO 1er CUATRI/Pensamiento Computacional/TPS/TPF/fotos/foto fondo menu.png')
Jugador_1_FOTO = pygame.image.load("C:/Users/joaco/OneDrive/Desktop/UDESA/primer AÑO 1er CUATRI/Pensamiento Computacional/TPS/TPF/fotos/auto 1.png")
JUGADOR_2_FOTO = pygame.image.load("C:/Users/joaco/OneDrive/Desktop/UDESA/primer AÑO 1er CUATRI/Pensamiento Computacional/TPS/TPF/fotos/auto 2.png")
COLOR_DE_FONDO = (34, 139, 34)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)

#Crear la pista
pista = Track(x_max=1000, y_max=800, width=65)

posicion_inicial_jugadores = pista.get_starting_position()
direction_inicial_jugadores = pista.get_starting_direction()

#JUGADOR 1
controles_Jugador_1 = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
Jugador_1 = PlayerCar("Colapinto", 5, controles_Jugador_1)



#JUGADOR 2
controles_jugador_2 = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
Jugador_2 = PlayerCar("Sainz", 10, controles_jugador_2)



def crear_vehiculo(x, y, color):
    return {"x": x, "y": y, "radius": 10, "color": color, "speed": Jugador_1.speed, "max_speed": Jugador_1.max_speed, "acceleration": Jugador_1.acceleration, "reducir velocidad": Jugador_1.reducir_velocidad, "direction": Jugador_1.direction, "angular_speed": Jugador_1.angular_speed}

def reiniciar_jugadores():
    Jugador_1 = crear_vehiculo(posicion_inicial_jugadores[0], posicion_inicial_jugadores[1], AZUL)
    Jugador_1["direction"] = math.degrees(direction_inicial_jugadores)

    Jugador_2 = crear_vehiculo(posicion_inicial_jugadores[0], posicion_inicial_jugadores[1] + 20, ROJO)
    Jugador_2["direction"] = math.degrees(direction_inicial_jugadores)
    return Jugador_1, Jugador_2

def mover_vehiculo(vehiculo, keys, controls):
    if keys[controls[0]]:  #Acelerar
        vehiculo["speed"] += vehiculo["acceleration"]
        vehiculo["speed"] = min(vehiculo["speed"], vehiculo["max_speed"])  #Limite de velocidad max
    elif keys[controls[1]]:  # Acelerar marcha atrás
        vehiculo["speed"] -= vehiculo["acceleration"]
        vehiculo["speed"] = max(vehiculo["speed"], -vehiculo["max_speed"] / 2)  #Limite velocidad max (marcha atras)
    else:
        #reducir velocidad
        if vehiculo["speed"] > 0:
            vehiculo["speed"] -= vehiculo["reducir velocidad"]
            vehiculo["speed"] = max(vehiculo["speed"], 0)
        elif vehiculo["speed"] < 0:
            vehiculo["speed"] += vehiculo["reducir velocidad"]
            vehiculo["speed"] = min(vehiculo["speed"], 0)

    if keys[controls[2]]:  #Girar izquierda
        vehiculo["direction"] += vehiculo["angular_speed"]

    if keys[controls[3]]:  #Girar derecha
        vehiculo["direction"] -= vehiculo["angular_speed"]

    # Convertir dirección a radianes
    radianes = math.radians(vehiculo["direction"])

    # Actualizar posición
    vehiculo["x"] += vehiculo["speed"] * math.cos(radianes)
    vehiculo["y"] -= vehiculo["speed"] * math.sin(radianes)  #Restar porque el eje Y apunta hacia abajo

    #Reducir velocidad fuera de la pista
    if not pista.is_point_inside_track([vehiculo["x"], vehiculo["y"]]):
        vehiculo["speed"] /= 10

    return vehiculo


def mostrar_menu():
    seleccion_de_modo = None

    while seleccion_de_modo is None:
        PANTALLA.blit(FOTO_FONDO_MENU, (0, 0))

        # Texto de instrucciones
        texto_1 = font.render("Presione 1 para un jugador", True, (255, 255, 255))
        texto_2 = font.render("Presione 2 para dos jugadores", True, (255, 255, 255))
        
        # Centrar el texto en la pantalla
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
                    seleccion_de_modo = 1
                elif event.key == pygame.K_2:
                    seleccion_de_modo = 2

        pygame.display.update()
    return seleccion_de_modo
    


#Configuración del tiempo (tick)
clock = pygame.time.Clock()
TICKS_POR_SEGUNDO = 100

#Inicialización de jugadores
Jugador_1, Jugador_2 = reiniciar_jugadores()
vueltas_Jugador_1, vueltas_jugador_2 = 0, 0
ultima_posicion_Jugador_1 = [Jugador_1["x"], Jugador_1["y"]]
ultima_posicion_jugador_2 = [Jugador_2["x"], Jugador_2["y"]]

#Modo de juego inicial
modo_de_juego = mostrar_menu()

#Bucle principal
running = True
while running:
    #Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_m and ganador is None:
            # Regresar al menú ("M")
            modo_de_juego = mostrar_menu()
            Jugador_1, Jugador_2 = reiniciar_jugadores()
            vueltas_Jugador_1, vueltas_jugador_2 = 0, 0 #Reiniciar vueltas

    #teclas presionadas
    keys = pygame.key.get_pressed()

    #Pintar el fondo
    PANTALLA.fill(COLOR_DE_FONDO)

    #Dibujar la pista
    if pista.track_polygon:
        # Parte exterior
        pygame.draw.polygon(PANTALLA, (128, 128, 128), list(pista.track_polygon.exterior.coords), 0)
        # Huecos en la pista
        for hole in pista.track_polygon.interiors:
            pygame.draw.polygon(PANTALLA, COLOR_DE_FONDO, list(hole.coords), 0)

        #Dibujar la línea de meta
        pygame.draw.line(PANTALLA, (255, 255, 255), (int(pista.finish_line.coords[0][0]), int(pista.finish_line.coords[0][1])), (int(pista.finish_line.coords[1][0]), int(pista.finish_line.coords[1][1])), 5,)

    if ganador is None:  # Si no hay un ganador, el juego sigue
        #Mover y dibujar el jugador 1
        trayectoria_Jugador_1 = [ultima_posicion_Jugador_1, [Jugador_1["x"], Jugador_1["y"]]]
        ultima_posicion_Jugador_1 = [Jugador_1["x"], Jugador_1["y"]]

        Jugador_1 = mover_vehiculo(Jugador_1, keys, controles_Jugador_1)
        pygame.draw.circle(PANTALLA, Jugador_1["color"], (int(Jugador_1["x"]), int(Jugador_1["y"])), Jugador_1["radius"])

        #Verificar si el jugador 1 cruzó la línea
        if pista.check_lap(trayectoria_Jugador_1):
            vueltas_Jugador_1 += 1
            if vueltas_Jugador_1 == 3:
                ganador = "Jugador 1"

        #Mover y dibujar el jugador 2
        if modo_de_juego == 2:
            trayectoria_jugador_2 = [ultima_posicion_jugador_2, [Jugador_2["x"], Jugador_2["y"]]]
            ultima_posicion_jugador_2 = [Jugador_2["x"], Jugador_2["y"]]

            Jugador_2 = mover_vehiculo(Jugador_2, keys, controles_jugador_2)
            pygame.draw.circle(PANTALLA, Jugador_2["color"],     (int(Jugador_2["x"]), int(Jugador_2["y"])), Jugador_2["radius"])

            #Verificar si el jugador 2 cruzó la línea
            if pista.check_lap(trayectoria_jugador_2):
                vueltas_jugador_2 += 1
                if vueltas_jugador_2 == 3:
                    ganador = "Jugador 2"

    else:  #mostrar mensaje de ganador
        texto_ganador = font_ganador.render(f"{ganador} es el ganador!", True, (255, 255, 0))
        texto_ganador_rect = texto_ganador.get_rect(center=(PANTALLA.get_width() // 2, PANTALLA.get_height() // 2))
        PANTALLA.blit(texto_ganador, texto_ganador_rect)

    #Dibujar las vueltas en pantalla
    texto_vueltas_1 = font.render(f"Jugador 1: {vueltas_Jugador_1} vueltas", True, (255, 255, 255))
    PANTALLA.blit(texto_vueltas_1, (10, 10)) 

    if modo_de_juego == 2:
        texto_vueltas_2 = font.render(f"Jugador 2: {vueltas_jugador_2} vueltas", True, (255, 255, 255))
        PANTALLA.blit(texto_vueltas_2, (10, 50))

    #Actualizar pantalla
    pygame.display.flip()

    #Controlar el tiempo del tick
    clock.tick(TICKS_POR_SEGUNDO)

pygame.quit()
