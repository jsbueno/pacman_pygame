import pygame


SIZE = 800, 600

def init():
    pygame.init()
    global Screen
    Screen = pygame.display.set_mode(SIZE)

def main():
    pygame.display.update()
    pygame.time.delay(700)


if __name__ == "__main__":
    init()
    try:
        main()
    finally:
        pygame.quit()
