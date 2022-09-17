import pygame

SIZE = 800, 600
CELL = 32

FPS = 30

def init():
    pygame.init()
    global Screen
    Screen = pygame.display.set_mode(SIZE)

def main():
    clock = pygame.time.Clock()

    x, y = 0, 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_LEFT:
                    x -= 1
                elif key == pygame.K_RIGHT:
                    x += 1
                if key == pygame.K_UP:
                    y -= 1
                elif key == pygame.K_DOWN:
                    y += 1
                if key == pygame.K_ESCAPE:
                    return

        pygame.draw.rect(Screen, (255, 255,0), (x * CELL, y * CELL, CELL, CELL))

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    init()
    try:
        main()
    finally:
        pygame.quit()
