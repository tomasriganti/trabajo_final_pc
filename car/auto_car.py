from car.car import Car

class AutoCar(Car):
    def __init__(self, driver_name: str, car_number: int):
        super().init(driver_name, car_number)

    def get_command(self, pygame_keys: dict, is_inside_track: bool) -> list[float]:
        """
        Returns the command for the car

        Args:
            pygame_keys (dict): The pygame keys
            is_inside_track (bool): Whether the car is inside the track

        Returns:
            list[float]: The command [acceleration, steering]
        """
        self.pygame_keys = pygame_keys
        self.is_inside_track = is_inside_track
