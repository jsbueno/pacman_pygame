import random
from pathlib import Path

import pygame

SIZE = 800, 600
CELL = 32

FPS = 30
WIDTH, HEIGHT = SIZE[0] // CELL, SIZE[1] // CELL

EMPTY = " "
WALL = "*"

def init():
    global Screen, BG
    pygame.init()
    Screen = pygame.display.set_mode(SIZE)
    BG = pygame.Surface(SIZE)
    BG.fill((0,0,0))

WALL_DIRECTIONS = {
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}

class Map:
    def __init__(self, data=None):
        self.size = WIDTH, HEIGHT
        self.data = data or ([EMPTY] * (WIDTH * HEIGHT))
        if not data:
            self.default_map_start()

    def default_map_start(self):
        self.random_map()
        self.frame()

    def random_map(self, seed=None, doors_per_col=3):
        seed = 0 if seed is None else seed

        for col in range(2, WIDTH - 1, 2):
            doors = set(random.sample(range(2, HEIGHT - 1, 2), doors_per_col))
            for row in range(0, HEIGHT, 2):
                self[col, row] = WALL
                if row not in doors:
                    direction = random.choice(list(WALL_DIRECTIONS.values()))
                    x = col + direction[0]
                    y = row + direction[1]
                    self[x, y] = WALL

    def frame(self):
        # linhas de cima e de baixo:
        for x in range(WIDTH):
            self[x, 0] = WALL
            self[x, HEIGHT - 1] = WALL

        for y in range(HEIGHT):
            self[0, y] = WALL
            self[WIDTH - 1, y] = WALL

    def __getitem__(self, pos):
        return self.data[pos[0] + pos[1] * self.size[0]]

    def __setitem__(self, pos, value):
        self.data[pos[0] + pos[1] * self.size[0]] = value

    def draw(self):
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if self[x, y] == WALL:
                    pygame.draw.rect(Screen, (255, 255, 255), (x * CELL, y * CELL, CELL, CELL))



class Character(pygame.sprite.Sprite):
    name = "pacman"

    def __init__(self, map, initial_pos=None):
        self.map = map
        self.ox, self.oy = self.x, self.y = initial_pos or (0,0)
        self.vx, self.vy = 0, 0
        self.load_assets()

        self.tick = 0
        self.anim_cycle = 10
        self.agility = 4

        super().__init__()

    def load_assets(self):
        path = Path(__file__).parent / "assets"
        pattern = f"{self.name}-left-{{:02d}}.png"
        i = 0
        image_list = []
        while True:
            full_path = path / pattern.format(i)
            if full_path.exists():
                img = pygame.image.load(full_path)
                scale = CELL / img.get_size()[0]
                img = pygame.transform.rotozoom(img, 0, scale)
                image_list.append(img)
            else:
                break
            i += 1
        self.images = image_list


    @property
    def rect(self):
        return pygame.Rect(self.x * CELL, self.y * CELL, CELL, CELL)

    @property
    def image(self):
        return self.images[self.tick // self.anim_cycle % 2]

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
        self.tick += 1
        if self.tick % self.agility != 0:
            return
        ox, oy = self.ox, self.oy = self.x, self.y
        x, y = self.x, self.y
        x_ok = y_ok = True

        x += self.vx
        y += self.vy
        if not (0 <= x < WIDTH) or not (0 <= y < HEIGHT):
            return

        if self.map[x, y] != EMPTY:
            if self.map[ox, y] == EMPTY:
                x_ok = False
            elif self.map[x, oy] == EMPTY:
                y_ok = False
            else:
                x_ok = y_ok = False
        if x_ok:
            self.x = x
        if y_ok:
            self.y = y


def main():
    clock = pygame.time.Clock()
    game_map = Map()

    character = Character(game_map, (1,1))
    characters = pygame.sprite.Group()
    characters.add(character)


    game_map.draw()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                character.move_event(event)
        characters.update()
        characters.clear(Screen, BG)
        characters.draw(Screen)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    init()
    try:
        main()
    finally:
        pygame.quit()
