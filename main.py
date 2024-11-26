import pygame
from shapely.geometry import Point
from track.track import Track
import math

pygame.init()

# Configuración del ícono y el nombre de la ventana
pygame.display.set_caption("F1 Simulation")
ICONO = pygame.image.load('C:/Users/joaco/OneDrive/Desktop/UDESA/primer AÑO 1er CUATRI/Pensamiento Computacional/TPS/TPF/fotos/f1 logo.png')
pygame.display.set_icon(ICONO)


# Configuración de la pantalla
PANTALLA = pygame.display.set_mode((1000, 800)) #(ancho, alto)

#Fotos y colores
FOTO_FONDO_MENU = pygame.image.load('C:/Users/joaco/OneDrive/Desktop/UDESA/primer AÑO 1er CUATRI/Pensamiento Computacional/TPS/TPF/fotos/foto fondo menu.png')
COLOR_DE_FONDO = (34, 139, 34)
JUGADOR_1_FOTO = pygame.image.load("C:/Users/joaco/OneDrive/Desktop/UDESA/primer AÑO 1er CUATRI/Pensamiento Computacional/TPS/TPF/fotos/auto 1.png")
JUGADOR_2_FOTO = pygame.image.load("C:/Users/joaco/OneDrive/Desktop/UDESA/primer AÑO 1er CUATRI/Pensamiento Computacional/TPS/TPF/fotos/auto 2.png")

# Crear la pista
pista = Track(x_max=1000, y_max=800, width=65)

# Inicialización de jugadores
def crear_vehiculo(x, y, color):
    return {"x": x, "y": y, "radius": 10, "color": color, "speed": 0, "max_speed": 0.5, "acceleration": 0.0025, "friction": 0.001, "direction": 0, "angular_speed": 0.5}

def reiniciar_jugadores():
    """Restablece las posiciones y atributos iniciales de los jugadores."""
    pos_1 = pista.get_starting_position()
    dir_1 = pista.get_starting_direction()
    jugador_1 = crear_vehiculo(pos_1[0], pos_1[1], (0, 0, 255))
    jugador_1["direction"] = math.degrees(dir_1)

    jugador_2 = crear_vehiculo(pos_1[0], pos_1[1] + 20, (255, 0, 0))
    jugador_2["direction"] = math.degrees(dir_1)
    return jugador_1, jugador_2

def mover_vehiculo(vehiculo, keys, controls):
    """Actualiza la posición y dirección del vehículo."""
    if keys[controls["up"]]:  # Acelerar hacia adelante
        vehiculo["speed"] += vehiculo["acceleration"]
        vehiculo["speed"] = min(vehiculo["speed"], vehiculo["max_speed"])  # Límite de velocidad máxima hacia adelante
    elif keys[controls["down"]]:  # Acelerar marcha atrás
        vehiculo["speed"] -= vehiculo["acceleration"]
        vehiculo["speed"] = max(vehiculo["speed"], -vehiculo["max_speed"] / 2)  # Límite de velocidad máxima marcha atrás
    else:
        # Aplicar fricción para reducir velocidad gradualmente
        if vehiculo["speed"] > 0:
            vehiculo["speed"] -= vehiculo["friction"]
            vehiculo["speed"] = max(vehiculo["speed"], 0)
        elif vehiculo["speed"] < 0:
            vehiculo["speed"] += vehiculo["friction"]
            vehiculo["speed"] = min(vehiculo["speed"], 0)

    if keys[controls["left"]]:  # Girar a la izquierda
        vehiculo["direction"] += vehiculo["angular_speed"]  # Sentido antihorario

    if keys[controls["right"]]:  # Girar a la derecha
        vehiculo["direction"] -= vehiculo["angular_speed"]  # Sentido horario

    # Convertir dirección a radianes
    radianes = math.radians(vehiculo["direction"])

    # Actualizar posición según la velocidad y dirección
    vehiculo["x"] += vehiculo["speed"] * math.cos(radianes)
    vehiculo["y"] -= vehiculo["speed"] * math.sin(radianes)  # Restar porque el eje Y apunta hacia abajo

    # Reducir velocidad si está fuera de la pista
    if not pista.is_point_inside_track([vehiculo["x"], vehiculo["y"]]):
        vehiculo["speed"] /= 10

    return vehiculo

# Controles de cada jugador
controles_jugador_1 = {"up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d}
controles_jugador_2 = {"up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT}

def mostrar_menu():
    """Muestra el menú inicial y devuelve el modo de juego seleccionado."""
    seleccion = None
    font = pygame.font.Font(None, 36)  # Fuente para el texto

    while seleccion is None:
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
                    seleccion = 1
                elif event.key == pygame.K_2:
                    seleccion = 2

        pygame.display.update()
    return seleccion

# Configuración del tiempo (tick)
clock = pygame.time.Clock()
TICKS_POR_SEGUNDO = 100

# Inicializar jugadores
Jugador_1, Jugador_2 = reiniciar_jugadores()
vueltas_jugador_1, vueltas_jugador_2 = 0, 0
ultima_posicion_jugador_1 = [Jugador_1["x"], Jugador_1["y"]]
ultima_posicion_jugador_2 = [Jugador_2["x"], Jugador_2["y"]]

# Modo de juego inicial
modo_de_juego = mostrar_menu()

# Bucle principal
running = True
while running:
    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            # Regresar al menú si se presiona "M"
            modo_de_juego = mostrar_menu()
            Jugador_1, Jugador_2 = reiniciar_jugadores()
            vueltas_jugador_1, vueltas_jugador_2 = 0, 0  # Reiniciar vueltas

    # Obtener teclas presionadas
    keys = pygame.key.get_pressed()

    # Dibujar fondo
    PANTALLA.fill(COLOR_DE_FONDO)

    # Dibujar la pista
    if pista.track_polygon:
        # Pista exterior
        pygame.draw.polygon(PANTALLA, (128, 128, 128), list(pista.track_polygon.exterior.coords), 0)
        # Huecos en la pista
        for hole in pista.track_polygon.interiors:
            pygame.draw.polygon(PANTALLA, COLOR_DE_FONDO, list(hole.coords), 0)

    # Mover y dibujar el jugador 1
    trayectoria_jugador_1 = [ultima_posicion_jugador_1, [Jugador_1["x"], Jugador_1["y"]]]
    ultima_posicion_jugador_1 = [Jugador_1["x"], Jugador_1["y"]]

    Jugador_1 = mover_vehiculo(Jugador_1, keys, controles_jugador_1)
    pygame.draw.circle(PANTALLA, Jugador_1["color"], (int(Jugador_1["x"]), int(Jugador_1["y"])), Jugador_1["radius"])

    # Mover y dibujar el jugador 2 si el modo es de 2 jugadores
    if modo_de_juego == 2:
        trayectoria_jugador_2 = [ultima_posicion_jugador_2, [Jugador_2["x"], Jugador_2["y"]]]
        ultima_posicion_jugador_2 = [Jugador_2["x"], Jugador_2["y"]]

        Jugador_2 = mover_vehiculo(Jugador_2, keys, controles_jugador_2)
        pygame.draw.circle(PANTALLA, Jugador_2["color"], (int(Jugador_2["x"]), int(Jugador_2["y"])), Jugador_2["radius"])

    # Actualizar pantalla
    pygame.display.flip()

    # Controlar el tiempo del tick
    clock.tick(TICKS_POR_SEGUNDO)

pygame.quit()
