import pygame
import os
import sys
import random

pygame.init()
current_path = os.path.dirname(__file__)
os.chdir(current_path)
WIDTH = 1500
HEIGHT = 700
FPS = 60
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('dino')

from loader import *


class Kaktus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = kaktus_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(WIDTH, WIDTH + 500)
        self.rect.bottom = HEIGHT - 60
        self.speed = 10
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_outline = self.mask.outline()
        self.mask_list = []

    def update(self):
        self.rect.x -= self.speed
        self.mask_list = []
        for i in self.mask_outline:
            self.mask_list.append((i[0] + self.rect.x, i[1] + self.rect.y))
        for point in self.mask_list:
            x = point[0]
            y = point[1]
            pygame.draw.circle(sc, 'green', (x, y), 3)
        if len(set(self.mask_list) & set(player.mask_list)) > 0:
            print('loser')


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.bottom = HEIGHT - 60
        self.jump = False
        self.jump_step = -22
        self.timer_spawn = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_outline = self.mask.outline()
        self.mask_list = []

    def update(self):
        global FPS
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            self.jump = True
        if self.jump:
            if self.jump_step <= 22:
                self.rect.y += self.jump_step
                self.jump_step += 1
            else:
                self.jump = False
                self.jump_step = -22
        self.timer_spawn += 1
        if self.timer_spawn / FPS > 2:
            kaktus = Kaktus()
            kaktus_group.add(kaktus)
            self.timer_spawn = 0
        if pygame.sprite.spritecollide(self, kaktus_group, True):
            self.kill()
            FPS = 0
            pygame.quit()
            sys.exit()
        self.mask_list = []
        for i in self.mask_outline:
            self.mask_list.append((i[0] + self.rect.x, i[1] + self.rect.y))
        for point in self.mask_list:
            x = point[0]
            y = point[1]
            pygame.draw.circle(sc, 'red', (x, y), 3)



def restart():
    global earth_group, kaktus_group, player_group, player
    earth_group = pygame.sprite.Group()
    kaktus_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    player = Player()
    player_group.add(player)


def lvl_game():
    sc.fill('gray')
    sc.blit(earth_image, (0, 650))
    player_group.update()
    player_group.draw(sc)
    kaktus_group.update()
    kaktus_group.draw(sc)
    pygame.display.update()


restart()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    lvl_game()
    clock.tick(FPS)
