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
    ox, oy = 0, 0
    vx, vy = 0, 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_LEFT:
                    vx = -1
                elif key == pygame.K_RIGHT:
                    vx = 1
                if key == pygame.K_UP:
                    vy = -1
                elif key == pygame.K_DOWN:
                    vy = 1
                if key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.KEYUP:
                key = event.key
                if key in (pygame.K_LEFT, pygame.K_RIGHT):
                    vx = 0
                if key in (pygame.K_UP, pygame.K_DOWN):
                    vy = 0
        x += vx
        y += vy

        pygame.draw.rect(Screen, (0, 0,0), (ox * CELL, oy * CELL, CELL, CELL))
        pygame.draw.rect(Screen, (255, 255,0), (x * CELL, y * CELL, CELL, CELL))

        ox, oy = x, y
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    init()
    try:
        main()
    finally:
        pygame.quit()
