import pygame

SIZE = 800, 600
CELL = 32

FPS = 30
WIDTH, HEIGHT = SIZE[0] // CELL, SIZE[1] // CELL

EMPTY = " "
WALL = "*"

def init():
    pygame.init()
    global Screen
    Screen = pygame.display.set_mode(SIZE)


class Map:
    def __init__(self, data=None):
        self.size = WIDTH, HEIGHT
        self.data = data or ([EMPTY] * (WIDTH * HEIGHT))
        if not data:
            self.default_map_start()

    def default_map_start(self):
        self[1, 1] = WALL

    def __getitem__(self, pos):
        return self.data[pos[0] + pos[1] * self.size[0]]

    def __setitem__(self, pos, value):
        self.data[pos[0] + pos[1] * self.size[0]] = value

    def draw(self):
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if self[x, y] == WALL:
                    pygame.draw.rect(Screen, (255, 255, 255), (x * CELL, y * CELL, CELL, CELL))



class Character:
    def __init__(self, map, initial_pos=None):
        self.map = map
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
        x, y = self.x, self.y

        x += self.vx
        y += self.vy
        if not (0 <= x < WIDTH) or not (0 <= y < HEIGHT):
            return

        if self.map[x, y]    != EMPTY:
            return

        self.x, self.y = x, y


    def draw(self):
        pygame.draw.rect(Screen, (0, 0, 0), (self.ox * CELL, self.oy * CELL, CELL, CELL))
        pygame.draw.rect(Screen, (255, 255,0), (self.x * CELL, self.y * CELL, CELL, CELL))


def main():
    clock = pygame.time.Clock()
    game_map = Map()

    character = Character(game_map)

    game_map.draw()
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
