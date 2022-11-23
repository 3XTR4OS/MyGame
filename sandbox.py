import pygame
import random
import os

# Game setting
WIDTH = 480
HEIGHT = 800
FPS = 60

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# WINDOW
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

# Assets
game_folder = os.path.dirname(r'P:/PyCharmProjects/MySuperGame')
img_folder = os.path.dirname(r'Assets/img/')
player_img = pygame.image.load(os.path.join(img_folder, 'p1_front.png')).convert()


def add_enemys(k=1):
    return [Enemy() for i in range(k)]


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.hp = 0
        self.speed = 5
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, WIDTH), 0)  # x,y

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()
            all_sprites.add(add_enemys(1))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - 44)

        self.step = 1

    def update(self):
        # self.rect.x += 12
        if self.rect.left > WIDTH:
            self.rect.right = 0

        elif self.rect.right < 0:
            self.rect.right = WIDTH

        elif self.rect.top > HEIGHT:
            self.rect.y = 0

        elif self.rect.bottom < 0:
            self.rect.y = HEIGHT

        # player.image.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))


# SPRITES
all_sprites = pygame.sprite.Group()
player = Player()
player2 = Player()
all_sprites.add(player)
all_sprites.add(add_enemys(3))

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player.rect.x += player.step

    if keys[pygame.K_LEFT]:
        player.rect.x -= player.step

    if keys[pygame.K_UP]:
        player.step += 2

    elif keys[pygame.K_DOWN]:
        if player.step >= 0:
            player.step -= 2
        else:
            player.step = 0



    if keys[pygame.K_a]:
        if player.step >= 0:
            player.step -= 0.1

    # Обновление
    all_sprites.update()
    print([list(i) for i in list(all_sprites)] if i)
    # Рендеринг
    screen.fill(BLUE)
    all_sprites.draw(screen)

    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

    # print(FPS)

pygame.quit()
