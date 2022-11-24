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


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(GREEN)
        self.speedy = 5
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x

    def update(self):
        self.rect.y -= self.speedy

        if self.rect.y < 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(4, 10)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)

        if self.rect.top > HEIGHT:
            self.speedy = random.randrange(4, 10)
            self.reset()

    def reset(self):
        self.rect.center = (random.randint(self.rect[-1], WIDTH), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - 44)

        self.speedx = 6

    def shoot(self):
        projectile = Projectile(self.rect.centerx, self.rect.top)
        all_sprites.add(projectile)
        projectiles.add(projectile)

    def update(self):

        # KEYS
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            player.rect.x += player.speedx

        if keys[pygame.K_LEFT]:
            player.rect.x -= player.speedx

        if keys[pygame.K_UP]:
            player.speedx += 2

        elif keys[pygame.K_DOWN]:
            if player.speedx >= 0:
                player.speedx -= 2
            else:
                player.speedx = 0

        if keys[pygame.K_a]:
            if player.speedx >= 0:
                player.speedx -= 0.1

        # OUT OF SCREEN
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.left < 0:
            self.rect.left = 0

        # SHOOT
        if keys[pygame.K_SPACE]:
            self.shoot()


# SPRITES
all_sprites = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
mobs = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(6):
    enemy = Enemy()
    all_sprites.add(enemy)
    mobs.add(enemy)

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    all_sprites.update()

    # hits
    hits = pygame.sprite.spritecollide(player, mobs, False)
    hits2 = pygame.sprite.groupcollide(projectiles, mobs, True, True)

    if hits:
        running = False

    for hit in hits2:
        enemy = Enemy()
        all_sprites.add(enemy)
        mobs.add(enemy)
    # Рендеринг
    screen.fill(BLUE)
    all_sprites.draw(screen)

    pygame.display.flip()

    # print(FPS)

pygame.quit()

