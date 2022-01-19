import pygame
import sys
import os


PPM = 20.0
TARGET_FPS = 60
TIME_STEP = 1.0 / TARGET_FPS


pygame.init()
FPS = 50
WIDTH = 1000
HEIGHT = 500
speed = 10


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

    fon = pygame.transform.scale(load_image('image\лес.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 100
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


fn = load_image("image\джунгли.jpg")

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
monster_group = pygame.sprite.Group()
money_group = pygame.sprite.Group()

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        if tile_type == "wall":
            self.image = load_image('image\земля2.png')
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)


class Monster(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(monster_group, all_sprites)
        self.image = load_image('image\pt.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.life = 2
        self.up_state = True

    def update(self):
        if self.up_state:
            self.rect.y -= 10
            if self.rect.y < 20:
                self.rect.y = 20
                self.up_state = False
        else:
            self.rect.y += 10
            for title in tiles_group:
                if pygame.sprite.collide_mask(self, title):
                    self.rect.bottom = title.rect.top
                    self.up_state = True


class Money(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(monster_group, all_sprites)
        self.image = load_image('image\star.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image('image\mar.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.jumpc = 10
        self.jump_state = False
        self.life = 10
        self.count = 0

    def move_char(self, ind):
        if ind == 1:
            self.rect.x += speed
        if ind == 2:
            self.rect.x -= speed
        if ind == 3:
            self.rect.y -= speed
        if ind == 4:
            self.rect.y += 100
        self.collide_with_platform(ind, tiles_group)
        self.collide_with_money(money_group)

    def change_j_state(self, state):
        self.jump_state = state

    def collide_with_platform(self, ind, ttl):
        for title in ttl:
            if pygame.sprite.collide_mask(self, title):
                if ind == 1:
                    self.rect.right = title.rect.left
                if ind == 2:
                    self.rect.left = title.rect.right
                if ind == 3:
                    self.rect.top = title.rect.bottom
                if ind == 4:
                    self.rect.bottom = title.rect.top

    def collide_with_monster(self, type):
        pass

    def collide_with_money(self, mn):
        for money in mn:
            if pygame.sprite.collide_mask(self, money):
                self.count += 1
                money.remove(money_group)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 4 - WIDTH // 6)


camera = Camera()


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
            elif level[y][x] == '$':
                Money(x, y)
            elif level[y][x] == '&':
                Monster(x, y)
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
                if event.key == pygame.K_SPACE:
                    player.jump_state = True
                if event.key == pygame.K_RIGHT:
                    player.move_char(1)
                if event.key == pygame.K_LEFT:
                    player.move_char(2)
                if event.key == pygame.K_DOWN:
                    player.move_char(4)

        if player.jump_state is True:
            if player.jumpc >= -10:
                player.rect.y -= player.jumpc
                player.jumpc -= 1
                player.collide_with_platform(4, tiles_group)
            else:
                player.jumpc = 10
                player.jump_state = False
                player.collide_with_platform(4, tiles_group)
        screen.blit(fn, (0, 0))
        all_sprites.draw(screen)
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        pygame.display.flip()
        clock.tick(20)

    pygame.quit()