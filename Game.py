import pygame
import sys
import os


pygame.init()

FPS = 25
WIDTH = 900
HEIGHT = 500
GRAVITY = 0.7


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Boba adventures')

clock = pygame.time.Clock()

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = (255, 255, 255)


all_sprites = pygame.sprite.Group()

tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
monster_group = pygame.sprite.Group()
money_group = pygame.sprite.Group()
flag_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()

tile_width = tile_height = 50


def load_image(name, color_key=None):
    try:
        fullname = os.path.join('data', name)
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print(f'В папке отсутствует файл: {name}')
        raise SystemExit(message)

    if color_key == -1:
        color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    elif color_key == "r":
        set_color(image, pygame.Color("red"))
    else:
        image = image.convert_alpha()
    return image


fn = load_image("jungle_2.jpg")


def set_color(img, color):
    for x in range(img.get_width()):
        for y in range(img.get_height()):
            color.a = img.get_at((x, y)).a
            img.set_at((x, y), color)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Приключения Бобы", "",
                  "Преодолевай препятствия и выигрывай", "чтобы передвигаться нажимай клавиши стрелок",
                  "чтобы одолевать монстров нажмите пробел", "наберите как можно больше очков"]

    fon = pygame.transform.scale(load_image('start.jpg'), (WIDTH, HEIGHT))
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


def dead_sreen():
    intro_text = ["Вы умерли", "",
                  "Нажмите кнопку мыши", "чтобы начать заново"]

    fon = pygame.transform.scale(load_image('death.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 200
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 250
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def end_screen(score):
    intro_text = [f"Вы набрали {score} очков", "", "СПАСИБО ЗА ИГРУ", "",
                  "ВОЗВРАЩАЙТЕСЬ", "ЗА НОВЫМИ ПРИКЛЮЧЕНИЯМИ!"]

    fon = pygame.transform.scale(load_image('end.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 150
    for line in intro_text:
        string_rendered = font.render(line, 100, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 200
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                terminate()  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def win_screen():
    intro_text = ["ПОЗДРАВЛЯЕМ", "",
                  "ВЫ ПЕРЕШЛИ НА НОВЫЙ УРОВЕНЬ"]

    fon = pygame.transform.scale(load_image('win (2).png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 150
    for line in intro_text:
        string_rendered = font.render(line, 100, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 200
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def load_level(name):
    filename = os.path.join('data', name)

    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        if tile_type == "wall":
            self.image = load_image('box.jpg')
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)


class Flag(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(flag_group, all_sprites)
        self.image = load_image('flag.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Monster(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(monster_group, all_sprites)
        self.frames = []
        self.cut_sheet(load_image("bird.png"), 3, 3)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        self.life = 2
        self.up_state = True

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

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
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Money(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(money_group, all_sprites)
        self.image = load_image('flower_.png', -1)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Lava(pygame.sprite.Sprite):
    def __init__(self, columns, rows, x, y):
        super().__init__(lava_group, all_sprites)
        self.x = x
        self.y = y
        self.frames = []
        self.cut_sheet(load_image("lava_2.png"), columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(tile_width * x, tile_height * y)
        self.mask = pygame.mask.from_surface(self.image)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.frames_right = []
        self.frames_left = []
        self.cut_sheet(load_image("char.png"), 8, 2)
        self.cur_frame = 0
        self.image = self.frames_left[self.cur_frame]
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

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for i in range(columns):
            frame_location = (self.rect.w * i, self.rect.h * 0)
            self.frames_right.append(sheet.subsurface(pygame.Rect(
                frame_location, self.rect.size)))
        for i in range(columns):
            frame_location = (self.rect.w * i, self.rect.h * 1)
            self.frames_left.append(sheet.subsurface(pygame.Rect(
                frame_location, self.rect.size)))

    def move_char(self, ind, jump, hit):
        if ind == 1:
            self.xspeed += 15
        if ind == 2:
            self.xspeed -= 15
        if ind == 0:
            self.xspeed = 0
        if jump:
            if self.onGround:
                self.yspeed -= self.jump_power
                self.onGround = False
        if not self.onGround:
            self.yspeed += GRAVITY

        self.onGround = False

        self.rect.y += self.yspeed
        self.collide_with_platform(0, self.yspeed, tiles_group)

        self.rect.x += self.xspeed
        self.collide_with_platform(self.xspeed, 0, tiles_group)

        self.collide_with_money(money_group)
        self.collide_with_monster(monster_group, hit)
        self.collide_with_lava(lava_group)

    def anim(self, ind):
        if ind == 1:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames_right)
            self.image = self.frames_right[self.cur_frame]
        if ind == 2:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames_left)
            self.image = self.frames_left[self.cur_frame]
        if ind == 0:
            self.image = self.frames_right[0]
        if ind == -1:
            self.image = self.frames_left[-1]

    def collide_with_platform(self, x_speed, y_speed, ttl):
        for title in ttl:
            if pygame.sprite.collide_mask(self, title):
                if x_speed > 0:
                    self.rect.right = title.rect.left
                if x_speed < 0:
                    self.rect.left = title.rect.right

                if y_speed < 0:
                    self.rect.top = title.rect.bottom
                    self.yspeed = 0

                if self.yspeed > 0:
                    self.rect.bottom = title.rect.top
                    self.onGround = True
                    self.yspeed = 0

    def collide_with_monster(self, mnstr, hit):
        for monster in mnstr:
            if pygame.sprite.collide_mask(self, monster):
                if hit == 1:
                    self.life -= 1
                else:
                    monster.life -= 1
                    self.score += 1
                monster.up_state = True

    def collide_with_money(self, mn):
        for money in mn:
            if pygame.sprite.collide_mask(self, money):
                self.coins_count += 1
                money.remove(money_group)
                money.remove(all_sprites)

    def collide_with_flag(self, flag):
        for f in flag:
            if pygame.sprite.collide_mask(self, f):
                return True

    def collide_with_lava(self, lava):
        for f in lava:
            if pygame.sprite.collide_mask(self, f):
                self.life = 0

    def die(self):
        if self.life <= 0:
            return True

    def show_info(self, screen, level, score):
        font = pygame.font.Font(None, 50)
        text = font.render(f"цветы: {self.coins_count}", True, (0, 0, 0))
        screen.blit(text, (5, 5))
        text_2 = font.render(f"жизнь: {self.life}", True, (0, 0, 0))
        screen.blit(text_2, (5, 50))
        text_3 = font.render(f"уровень: {level}", True, (0, 0, 0))
        screen.blit(text_3, (650, 5))
        text_4 = font.render(f"счет: {score}", True, (0, 0, 0))
        screen.blit(text_4, (650, 50))


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

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
            elif level[y][x] == '!':
                Flag(x, y)
            elif level[y][x] == '%':
                Lava(5, 1, x, y)
    return new_player, x, y


levels = ["level.txt", "level_2.txt", "level_3.txt"]
start_screen()
cur_level = 1
player, level_x, level_y = generate_level(load_level(levels[cur_level - 1]))
running = True
up = False
hitting = 1
score = 0
cur_ind = 0
cur_st = 0
while running:
    while running:
        cur_ind = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_screen(score)
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    up = True
                if event.key == pygame.K_RIGHT:
                    cur_ind = 1
                    cur_st = 1
                if event.key == pygame.K_LEFT:
                    cur_ind = 2
                    cur_st = 2
                if event.key == pygame.K_SPACE:
                    hitting = 2
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    cur_ind = 0
                    cur_st = 0
                if event.key == pygame.K_LEFT:
                    cur_ind = 0
                    cur_st = -1
                if event.key == pygame.K_SPACE:
                    hitting = 1
                if event.key == pygame.K_UP:
                    up = False

        player.move_char(cur_ind, up, hitting)
        screen.blit(fn, (0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        camera.update(player)
        player.anim(cur_st)
        for sprite in all_sprites:
            camera.apply(sprite)
        player.show_info(screen, cur_level, score)
        if player.collide_with_flag(flag_group):
            cur_level += 1
            score += player.life * 5
            score += player.coins_count * 2
            score += player.score
            for elem in tiles_group:
                elem.remove(tiles_group)
                elem.remove(all_sprites)
            for elem in monster_group:
                elem.remove(monster_group)
                elem.remove(all_sprites)
            for elem in player_group:
                elem.remove(player_group)
                elem.remove(all_sprites)
            for elem in lava_group:
                elem.remove(lava_group)
                elem.remove(all_sprites)
            for elem in flag_group:
                elem.remove(flag_group)
                elem.remove(all_sprites)
            for elem in money_group:
                elem.remove(money_group)
                elem.remove(all_sprites)
            if cur_level == 4:
                end_screen(score)
            else:
                player, level_x, level_y = generate_level(load_level(levels[cur_level - 1]))
                win_screen()

        if player.die():
            for elem in tiles_group:
                elem.remove(tiles_group)
                elem.remove(all_sprites)
            for elem in monster_group:
                elem.remove(monster_group)
                elem.remove(all_sprites)
            for elem in player_group:
                elem.remove(player_group)
                elem.remove(all_sprites)
            for elem in lava_group:
                elem.remove(lava_group)
                elem.remove(all_sprites)
            for elem in flag_group:
                elem.remove(all_sprites)
                elem.remove(flag_group)
            for elem in money_group:
                elem.remove(all_sprites)
                elem.remove(money_group)
            dead_sreen()
            player, level_x, level_y = generate_level(load_level(levels[cur_level - 1]))
            up = False
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()