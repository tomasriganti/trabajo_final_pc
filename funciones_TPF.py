import pygame
import time

def mostrar_menu(pant, foto, fuente):
    while True:
        pant.blit(foto, (0, 0))
        texto_menu = fuente.render("Presiona '1' para jugar con un jugador '2' para jugar con dos jugadores", True, (255, 255, 255))
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
                

def mostrar_contador(pant, fuente, color, duracion, color_fondo):
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
    pygame.mixer.init()
    sonido = pygame.mixer.Sound(ruta_sonido)
    sonido.play()


def mensaje_ganador(resultado, pant, color_fondo, fuente, color, sonido):
    if resultado:
        mensaje_ganador = fuente.render(f"¡{resultado} gana!", True, color)
        pant.fill(color_fondo)
        pant.blit(mensaje_ganador, (pant.get_width() // 2 - mensaje_ganador.get_width() // 2, pant.get_height() // 2 - mensaje_ganador.get_height() // 2))
        pygame.display.update()
        reproducir_sonido(sonido)
        time.sleep(5)