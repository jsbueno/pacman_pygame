import pygame

SIZE = 800, 600
CELL = 32

FPS = 30
WIDTH, HEIGHT = SIZE[0] // CELL, SIZE[1] // CELL

def init():
    pygame.init()
    global Screen
    Screen = pygame.display.set_mode(SIZE)

class Character:
    def __init__(self, initial_pos=None):
        self.ox, self.oy = self.x, self.y = initial_pos or (0,0)
        self.vx, self.vy = 0, 0

    def move_event(self, event):
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_LEFT:
                self.vx = -1
            elif key == pygame.K_RIGHT:
                self.vx = 1
            if key == pygame.K_UP:
                self.vy = -1
            elif key == pygame.K_DOWN:
                self.vy = 1
        if event.type == pygame.KEYUP:
            key = event.key
            if key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.vx = 0
            if key in (pygame.K_UP, pygame.K_DOWN):
                self.vy = 0

    def update(self):
        self.ox, self.oy = self.x, self.y

        if 0 <= self.x + self.vx < WIDTH:
            self.x += self.vx
        if 0 <= self.y + self.vy < HEIGHT:
            self.y += self.vy

    def draw(self):
        pygame.draw.rect(Screen, (0, 0,0), (self.ox * CELL, self.oy * CELL, CELL, CELL))
        pygame.draw.rect(Screen, (255, 255,0), (self.x * CELL, self.y * CELL, CELL, CELL))


def main():
    clock = pygame.time.Clock()

    character = Character()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                character.move_event(event)
        character.update()
        character.draw()

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    init()
    try:
        main()
    finally:
        pygame.quit()
