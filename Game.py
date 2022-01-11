import pygame
import sys
import os

pygame.init()
FPS = 50
WIDTH = 700
HEIGHT = 400
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


tile_images = {
    'wall': load_image('img_1.png'), "empty": None}

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
sprite.rect.y = 290



def move_char(ind):
    if ind == 1:
        sprite.rect.x += 20
    if ind == 2:
        sprite.rect.x -= 20
    if ind == 3:
        sprite.rect.y -= 20"""


fn = load_image("img_2.png")

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = (255, 255, 255)


level = [
       "                        -",
       "                        -",
       "                        -",
       "             --         -",
       "                        -",
       "                        -",
       "                        -",
       "                    --- -",
       "                        -",
       "                        -",
       "       ---              -",
       "-------------------------"]

start_screen()

running = True
while running:
    while running:
        all_sprites.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                """if event.key == pygame.K_RIGHT:
                    move_char(1)
                if event.key == pygame.K_LEFT:
                    move_char(2)
                if event.key == pygame.K_UP:
                    move_char(3)"""
        screen.blit(fn, (0, 0))
        x = y = 0  # координаты
        for row in level:  # вся строка
            for col in row:  # каждый символ
                if col == "-":
                    pf = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
                    pf.fill(pygame.Color(PLATFORM_COLOR))
                    screen.blit(pf, (x, y))

                x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
            y += PLATFORM_HEIGHT  # то же самое и с высотой
            x = 0  # на каждой новой с
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(50)

    pygame.quit()
