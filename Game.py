import pygame
import sys
import os

pygame.init()
FPS = 50
WIDTH = 1000
HEIGHT = 500
speed = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()


def load_image(name, color_key=None):
    try:
        fullname = os.path.join(name)
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print(f'В папке отсутствует файл: {name}')
        raise SystemExit(message)

    if color_key == -1:
        color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Приключения Бобы", "",
                  "Преодолевай препятствия и выигрывай"]

    fon = pygame.transform.scale(load_image('img.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


"""tile_images = {
    'wall': load_image('img_1.png'), "empty": None}"""

"""all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()



def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
"""

"""all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
sprite.image = pygame.transform.scale(load_image("tst.png"), (100, 100))
sprite.rect = (sprite.image.get_rect())
all_sprites.add(sprite)


sprite.rect.x = 5
sprite.rect.y = 290"""



def move_char(ind, pl):
    if ind == 1:
        pl.rect.x += 20
    if ind == 2:
        pl.rect.x -= 20
    if ind == 3:
        pl.rect.y -= 20


fn = load_image("img_2.png")

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = (255, 255, 255)


def load_level(filename):
    filename = filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        if tile_type == "wall":
            self.image = load_image('box.png')
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)


player_image = load_image('mar.png')


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
    return new_player, x, y


start_screen()
player, level_x, level_y = generate_level(load_level('level.txt'))
running = True
while running:
    while running:
        all_sprites.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    move_char(1, player)
                if event.key == pygame.K_LEFT:
                    move_char(2, player)
                if event.key == pygame.K_UP:
                    move_char(3, player)
        screen.blit(fn, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(50)

    pygame.quit()
