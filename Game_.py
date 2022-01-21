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
speed = 15

JUMP_POWER = 10
GRAVITY = 0.8


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
monster_group = pygame.sprite.Group()
money_group = pygame.sprite.Group()

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        if tile_type == "wall":
            self.image = load_image('box.png')
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)


class Monster(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(monster_group, all_sprites)
        self.image = load_image('pt.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.life = 2
        self.up_state = True

    def update(self):
        if self.life <= 0:
            self.remove(all_sprites)
            self.remove(monster_group)

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
        super().__init__(money_group, all_sprites)
        self.image = load_image('star.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

MOVE_SPEED = 7



class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image('mar.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.jump_power = 10
        self.jump_state = False
        self.life = 10
        self.score = 0
        self.coins_count = 0
        self.yspeed = 0
        self.xspeed = 15
        self.onGround = True
        self.xvel = 0

    def update(self, left, right):
        if left:
            self.xvel = -MOVE_SPEED  # Лево = x- n

        if right:
            self.xvel = MOVE_SPEED  # Право = x + n

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0

        self.rect.x += self.xvel  # переносим свои положение на xvel

    def draw(self, screen):  # Выводим себя на экран
        screen.blit(self.image, (self.rect.x, self.rect.y))
        self.rect.x += self.xspeed
        self.collide_with_platform(self.xspeed, 0, tiles_group)
        self.collide_with_money(money_group)



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
left = right = False    # по умолчанию — стоим
while running:
    while running:
        all_sprites.update()
        hitting = 1
        up = False
        cur_ind = 0
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
                left = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
                right = True

            if e.type == pygame.KEYUP and e.key == pygame.K_RIGHT:
                right = False
            if e.type == pygame.KEYUP and e.key == pygame.K_LEFT:
                left = False

        """if player.jump_state is True:
            if player.jumpc >= -10:
                player.rect.y -= player.jumpc
                player.jumpc -= 1
                player.collide_with_platform(4, tiles_group)
            else:
                player.jumpc = 10
                player.jump_state = False
                player.collide_with_platform(4, tiles_group)
        player.collide_with_monster(monster_group, hitting)"""
        player.update(left, right)  # передвижение
        player.draw(screen)  # отобр
        pygame.display.flip()
        clock.tick(20)
    pygame.quit()