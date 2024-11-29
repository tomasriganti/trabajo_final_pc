from shapely.geometry import LineString, Polygon
import math

# Crear vehículo IA
def crear_vehiculo_ia(x, y, color):
    return {"x": x, "y": y, "radius": 10, "color": color, "speed": 0.3, "max_speed": 0.4, 
            "acceleration": 0.0025, "friction": 0.001, "direction": 0, "angular_speed": 0.5}

# Mover vehículo IA
def mover_vehiculo_ia(vehiculo, pista):
    angulos_sensores = [-90, -45, 0, 45, 90]  # Sensores en más direcciones para mejor detección
    distancia_sensor = 75  # Sensores más largos para anticipar bordes

    # Lista de colisiones detectadas por los sensores
    colisiones = []
    for angulo in angulos_sensores:
        radianes = math.radians(vehiculo["direction"] + angulo)
        punto_sensor = (vehiculo["x"] + distancia_sensor * math.cos(radianes),
                        vehiculo["y"] - distancia_sensor * math.sin(radianes))
        sensor_linea = LineString([(vehiculo["x"], vehiculo["y"]), punto_sensor])

        # Detectar intersección con la pista
        if sensor_linea.intersects(pista):
            colisiones.append(angulo)

    # Ajustar dirección para evitar colisiones
    if colisiones:
        # Gira en dirección opuesta a la primera colisión detectada
        vehiculo["direction"] += vehiculo["angular_speed"] * (1 if colisiones[0] > 0 else -1)
        vehiculo["speed"] *= 0.8  # Reduce la velocidad al evitar bordes
    else:
        # Si no hay colisiones, acelera y avanza
        vehiculo["speed"] = min(vehiculo["speed"] + vehiculo["acceleration"], vehiculo["max_speed"])

    # Actualizar posición
    radianes = math.radians(vehiculo["direction"])
    vehiculo["x"] += vehiculo["speed"] * math.cos(radianes)
    vehiculo["y"] -= vehiculo["speed"] * math.sin(radianes)

    # Si el vehículo está atrapado (colisiones en todos los sensores), gira para liberarse
    if len(colisiones) == len(angulos_sensores):
        vehiculo["direction"] += vehiculo["angular_speed"]

    return vehiculo

# Función para dibujar sensores (opcional, para depuración)
def dibujar_sensores(pantalla, vehiculo, angulos_sensores, distancia_sensor):
    for angulo in angulos_sensores:
        radianes = math.radians(vehiculo["direction"] + angulo)
        punto_sensor = (vehiculo["x"] + distancia_sensor * math.cos(radianes),
                        vehiculo["y"] - distancia_sensor * math.sin(radianes))
        pygame.draw.line(pantalla, (255, 0, 0), (vehiculo["x"], vehiculo["y"]), punto_sensor, 2)
