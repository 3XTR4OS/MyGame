import os
import random
import time

import pygame

# S E T T I N G S
WIDTH = 800
HEIGHT = 800
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 183, 235)

scroll = [0, 0]

# A S S E T S
game_folder = os.path.dirname(r'P:\\PyCharmProjects\\MySuperGame')
img_folder = os.path.dirname(r'Assets\\img\\')
player_img_folder = os.path.join(img_folder, 'player_imgs')
bg = pygame.image.load('Assets\\img\\background\\bg2.jpg').convert()
enemy_img = pygame.image.load('Assets\\img\\player_imgs\\Enemy2.png')
crosshair_img = pygame.image.load('Assets\\img\\crosshair.png').convert()
crosshair_img.set_colorkey(BLACK)

white_fire_folder = os.path.join(img_folder, r'projectiles\\white_fire')


# animation_set = [pygame.image.load(f'{white_fire_folder}\\f{i}.png') for i in range(1, 6 + 1)]


class Projectile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.anim_count = 0
        self.animation_set = [pygame.image.load(f'{white_fire_folder}\\f{i}.png') for i in range(2, 6 + 1)]
        if player.walkLeft:
            self.animation_set = [pygame.transform.flip(i, True, False) for i in self.animation_set]

        self.image = self.animation_set[self.anim_count // 12]
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y

        # mouse_x, mouse_y = pygame.mouse.get_pos()
        self.speed = 10
        mouse_x, mouse_y = pygame.mouse.get_pos()  # offset_pos = sprite.rect.topleft - self.offset

        self.speed_x = (mouse_x - (player.rect.topleft[0] - camera_group.offset.x)) // self.speed
        self.speed_y = (mouse_y - (player.rect.topleft[1] - camera_group.offset.y)) // self.speed
        print(camera_group.offset.x)
        print(camera_group.offset.y)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # A N I M A T I O N
        self.image = self.animation_set[self.anim_count // 12]
        self.image.set_colorkey(BLACK)

        if self.anim_count + 1 >= 60:
            self.anim_count = 0
            self.kill()

        self.anim_count += 1

        if self.rect.y < 0 or self.rect.y > HEIGHT or self.rect.x < 0 or self.rect.x > WIDTH:
            self.kill()


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = pygame.display.get_window_size()[0] // 2
        self.half_h = pygame.display.get_window_size()[1] // 2

        # ground
        self.ground_surf = bg
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def custom_draw(self, _player):
        self.center_target_camera(_player)
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf, ground_offset)

        # ENEMY OBJECTS COLLISION START
        for sprite in self.sprites():
            if sprite in enemy_group:

                for sprite1 in self.sprites():
                    if sprite1 in enemy_group:

                        if sprite != sprite1:
                            if sprite.rect.colliderect(sprite1.rect):
                                speed = sprite.speed * 1.5
                                if sprite1.directionx == 'RIGHT':
                                    sprite1.rect.x -= speed

                                elif sprite1.directionx == 'LEFT':
                                    sprite1.rect.x += speed

                                if sprite1.directiony == 'UP':
                                    sprite1.rect.y += speed

                                elif sprite1.directiony == 'DOWN':
                                    sprite1.rect.y -= speed

                                # sprite.image.fill(CYAN)

                            # else:
                                # sprite.image.fill(RED)
            # ENEMY OBJECTS COLLISION END

            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
            self.display_surface.blit(crosshair_img, pygame.mouse.get_pos())


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        # self.image = pygame.Surface((50, 50))
        # self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.y = random.randint(0, pygame.display.get_window_size()[0])
        self.rect.x = random.randint(0, pygame.display.get_window_size()[1])
        self.speed = random.randint(1, 2)
        self.directionx = 'LEFT'
        self.directiony = 'UP'

    def update(self):
        if self.rect.centerx < player.rect.x:
            self.rect.centerx += self.speed
            self.directionx = 'RIGHT'
        elif self.rect.centerx > player.rect.x:
            self.rect.centerx -= self.speed
            self.directionx = 'LEFT'
        else:
            self.rect.centerx += 1

        if self.rect.centery > player.rect.y:
            self.rect.centery -= self.speed
            self.directiony = 'UP'
        elif self.rect.centery < player.rect.y:
            self.rect.centery += self.speed
            self.directiony = 'DOWN'
        else:
            self.rect.centery += 1

    def mob_reset(self):
        enem = Enemy()
        camera_group.add(enem)
        enemy_group.add(enem)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.animation_set = [pygame.image.load(f"{player_img_folder}\\p{i}.png") for i in range(1, 5 + 1)]
        self.anim_count = 0
        self.image = self.animation_set[self.anim_count]
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2
        self.rect.y = HEIGHT / 2
        self.walkLeft = False
        self.walkRight = True
        self.speed = 4

    def update(self):

        key = pygame.key.get_pressed()
        # print(f'--{self.anim_count}--{self.anim_count // 12}')

        # A N I M A T I O N
        if player.walkRight:
            self.image = self.animation_set[self.anim_count // 6]

        elif player.walkLeft:
            transformed_image = pygame.transform.flip(self.animation_set[self.anim_count // 6], True, False)
            self.image = transformed_image

        if self.anim_count + 1 >= 30:
            self.anim_count = 0

        self.anim_count += 1

        # K E Y S
        if key[pygame.K_d]:
            self.rect.x += self.speed
            self.walkRight = True
            self.walkLeft = False

        elif key[pygame.K_a]:
            self.rect.x -= self.speed
            self.walkRight = False
            self.walkLeft = True

        if key[pygame.K_w]:
            self.rect.y -= self.speed

        if key[pygame.K_s]:
            self.rect.y += self.speed


# SPRITES
projectiles = pygame.sprite.Group()
camera_group = CameraGroup()
enemy_group = pygame.sprite.Group()

player = Player()
camera_group.add(player)

for i in range(200):
    enem = Enemy()
    camera_group.add(enem)
    enemy_group.add(enem)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                projectile = Projectile()
                projectiles.add(projectile)
                camera_group.add(projectile)

    # camera & drawing
    camera_group.update()
    camera_group.custom_draw(player)

    # H I T S
    # player_dead = pygame.sprite.spritecollide(player, enemy_group, False, False)
    # if player_dead:
    #     running = False
    #     print('ВЫ УМЕРЛИ \n' * 10)

    enemy_hit = pygame.sprite.groupcollide(projectiles, enemy_group, True, True)
    if enemy_hit:
        Enemy.mob_reset(Enemy())

    # pygame stuff
    pygame.display.update()
    clock.tick(FPS)
