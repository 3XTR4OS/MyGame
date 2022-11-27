import os
import time
import pygame

# SETTING
WIDTH = 800
HEIGHT = 800
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# ASSETS
game_folder = os.path.dirname(r'P:\\PyCharmProjects\\MySuperGame')
img_folder = os.path.dirname(r'Assets\\img\\')
player_img_folder = os.path.join(img_folder, 'player_imgs')
print(player_img_folder)
# player_img = pygame.image.load(os.path.join(img_folder, 'p_sprite.png')).convert()
# background_img = pygame.image.load(os.path.)

# animation_set = [pygame.image.load(f"{player_img_folder}p{i}.png") for i in range(1, 6)]

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 183, 235)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.animation_set = [pygame.image.load(f"{player_img_folder}\\p{i}.png") for i in range(1, 6)]
        self.anim_count = 0
        # self.image = pygame.Surface((0, 1))
        self.image = self.animation_set[self.anim_count]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2
        self.rect.y = HEIGHT / 2
        self.speed = 4
        self.walkLeft = False
        self.walkRight = False

    def update(self):
        key = pygame.key.get_pressed()
        print(f'--{self.anim_count}--{self.anim_count // 6}')

        if self.anim_count + 1 >= 60:
            self.anim_count = 0

        # screen.blit(animation_set[self.anim_count // 20], (self.rect.x, self.rect.y))
        self.anim_count += 1

        if key[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.walkRight = True
            self.walkLeft = False

        elif key[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.walkRight = False
            self.walkLeft = True
            # self.screen.blit(pygame.transform.flip(self.image, True, False), self.rect)

        if key[pygame.K_UP]:
            self.rect.y -= self.speed

        if key[pygame.K_DOWN]:
            self.rect.y += self.speed


def draw_window():
    # sprites
    all_sprites.draw(screen)

    # screen
    screen.fill(CYAN)

    # player
    # if player.walkLeft:
    #     pygame.transform.flip(player.image, True, False)

    screen.blit(player.animation_set[player.anim_count // 12], (player.rect.x, player.rect.y))

    pygame.display.update()


# SPRITES
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    draw_window()
