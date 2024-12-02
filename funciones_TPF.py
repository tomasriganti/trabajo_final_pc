import pygame
import time


def mostrar_menu(pant: pygame.Surface, foto: pygame.Surface, fuente: pygame.font.Font) -> int:
    """
    Muestra un menú en la pantalla para seleccionar el modo de juego.

    Args:
        pant (pygame.Surface): La superficie de la pantalla donde se renderiza el menú.
        foto (pygame.Surface): Imagen de fondo para el menú.
        fuente (pygame.font.Font): Fuente utilizada para el texto del menú.

    Returns:
        int: 1 si se selecciona el modo de un jugador, 2 si se selecciona el modo de dos jugadores.
    """
    while True:
        pant.blit(foto, (0, 0))
        texto_menu = fuente.render(
            "Presiona '1' para jugar con un jugador '2' para jugar con dos jugadores",
            True, 
            (255, 255, 255)
        )
        pant.blit(texto_menu, (50, 700))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Jugar con un jugador
                    return 1
                elif event.key == pygame.K_2:  # Jugar con dos jugadores
                    return 2


def mostrar_contador(pant: pygame.Surface, fuente: pygame.font.Font, color: tuple[int, int, int], duracion: int, color_fondo: tuple[int, int, int]) -> None:
    """
    Muestra un contador regresivo en la pantalla.

    Args:
        pant (pygame.Surface): La superficie de la pantalla donde se muestra el contador.
        fuente (pygame.font.Font): Fuente utilizada para el texto del contador.
        color (tuple[int, int, int]): Color del texto del contador en formato RGB.
        duracion (int): Duración del contador regresivo en segundos.
        color_fondo (tuple[int, int, int]): Color de fondo de la pantalla en formato RGB.
    """
    for i in range(duracion, 0, -1):
        pant.fill(color_fondo)
        texto_contador = fuente.render(str(i), True, color)
        pant.blit(
            texto_contador,
            (pant.get_width() // 2 - texto_contador.get_width() // 2,
             pant.get_height() // 2 - texto_contador.get_height() // 2)
        )
        pygame.display.update()
        time.sleep(1)


def reproducir_sonido(ruta_sonido: str) -> None:
    """
    Reproduce un archivo de sonido.

    Args:
        ruta_sonido (str): Ruta del archivo de sonido a reproducir.
    """
    pygame.mixer.init()
    sonido = pygame.mixer.Sound(ruta_sonido)
    sonido.play()


def mensaje_ganador(resultado: str, pant: pygame.Surface, color_fondo: tuple[int, int, int], fuente: pygame.font.Font, color: tuple[int, int, int], sonido: str) -> None:
    """
    Muestra un mensaje de ganador en la pantalla.

    Args:
        resultado (str): Nombre o identificación del ganador.
        pant (pygame.Surface): La superficie de la pantalla donde se muestra el mensaje.
        color_fondo (tuple[int, int, int]): Color de fondo de la pantalla en formato RGB.
        fuente (pygame.font.Font): Fuente utilizada para el texto del mensaje.
        color (tuple[int, int, int]): Color del texto del mensaje en formato RGB.
        sonido (str): Ruta del archivo de sonido que se reproducirá al mostrar el mensaje.
    """
    if resultado:
        mensaje_ganador = fuente.render(f"¡{resultado} gana!", True, color)
        pant.fill(color_fondo)
        pant.blit(
            mensaje_ganador,
            (pant.get_width() // 2 - mensaje_ganador.get_width() // 2,
             pant.get_height() // 2 - mensaje_ganador.get_height() // 2)
        )
        pygame.display.update()
        reproducir_sonido(sonido)
        time.sleep(5)
