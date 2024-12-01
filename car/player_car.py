from car.car import Car

import math

class PlayerCar(Car):
    def __init__(self, driver_name: str, car_number: int, movement_keys: list):
        """
        Initializes the player car

        Args:
            driver_name (str): The name of the driver
            car_number (int): The number of the car
            movement_keys (list): The keys for the movement [up, down, left, right]. 
                                  Probably something like [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
        """
        super().init(driver_name, car_number)
        self.movement_keys = movement_keys

    def get_command(self, pygame_keys, is_inside_track):
        """
        Returns the command for the car

        Args:
            pygame_keys (dict): The pygame keys
            is_inside_track (bool): Whether the car is inside the track

        Returns:
            list[float]: The command [acceleration, steering]
        """
        if pygame_keys[self.movement_keys[0]]:  # Acelerar
            self.speed += self.acceleration
            self.speed = min(self.speed, self.max_speed)  # velocidad máx
        elif pygame_keys[self.movement_keys[1]]:  # marcha atrás
            self.speed -= self.acceleration
            self.speed = max(self.speed, -self.max_speed / 2)  # Límite marcha atrás
        else:
            # Reducir velocidad
            if self.speed > 0:
                self.speed -= self.reducir_velocidad
                self.speed = max(self.speed, 0)
            elif self.speed < 0:
                self.speed += self.reducir_velocidad
                self.speed = min(self.speed, 0)

        if pygame_keys[self.movement_keys[2]]:  # Girar izquierda
            self.direction -= math.radians(self.steer)

        if pygame_keys[self.movement_keys[3]]:  # Girar derecha
            self.direction += math.radians(self.steer)

        return [self.acceleration, self.steer]
