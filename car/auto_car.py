from car.car import Car
import math

class AutoCar(Car):
    def __init__(self, driver_name: str, car_number: int):
        super().init(driver_name, car_number)

    def get_command(self, distances: list, is_inside_track: bool) -> list[float]:
        """
        Returns the command for the car

        Args:
            pygame_keys (dict): The pygame keys
            is_inside_track (bool): Whether the car is inside the track

        Returns:
            list[float]: The command [acceleration, steering]
        """
        self.speed += self.acceleration
        self.speed = min(self.speed, self.max_speed)

        if distances[0] is None:
            self.direction -= math.radians(self.steer)

        elif distances[1] is None:
            self.direction += math.radians(self.steer)

        if distances[0] < 35:
            self.speed -= self.acceleration
            self.direction -= math.radians(self.steer)

        elif distances[1] < 35:
            self.speed -= self.acceleration
            self.direction += math.radians(self.steer)

        elif distances[0] < 15:
            self.speed = 0
            self.direction -= math.radians(self.steer)

        elif distances[1] < 15:
            self.speed = 0
            self.direction += math.radians(self.steer)

        else:
            if distances[0] < distances[1]:  # Girar izquierda
                self.direction -= math.radians(self.steer)

            if distances[0] > distances[1]:  # Girar derecha
                self.direction += math.radians(self.steer)

        return [self.acceleration, self.steer]
