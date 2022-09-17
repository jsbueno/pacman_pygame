import pygame


SIZE = 800, 600

FPS = 30

def init():
    pygame.init()
    global Screen
    Screen = pygame.display.set_mode(SIZE)

def main():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        pygame.draw.rect(Screen, (255, 255,0), (64,64,32,32))

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    init()
    try:
        main()
    finally:
        pygame.quit()
