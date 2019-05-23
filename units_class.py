# -*- coding: utf-8 -*-

import pygame
from random import randint
# import numpy as np

unitno = 0
# Размер карты
map_x = 900
map_y = 900
# map_array = np.zeros((map_x, map_y))
# Окно
window = pygame.display.set_mode((map_x, map_y+30))    # Окно (холст 400 + строка состояния 30)
pygame.display.set_caption('Emunation')    # Имя окна
# Холст
screen = pygame.Surface((map_x, map_y))             # Игровой экран|холст
# Строка состояния
info_string = pygame.Surface((map_x, 30))

# програмная отрисовка юнита
class NationUnit(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, color, width, height, family='Snow'):
        # coding
        global unitno
        self.unitno = unitno
        unitno += 1
        self.x = xpos
        self.y = ypos
        self.xvel = 1
        self.yvel = 1
        self.width = width
        self.height = height
        self.color = color
        self.family = family
    # Пол
        if randint(0, 1) == 0:
            self.sex = 'Male'
        else:
            self.sex = 'Female'
    # Встреченные юниты
        self.today_meeted_unit = []
    # Беременность
        self.pregnancy = False
        self.pregnancy_day = 0
        self.child = []
        # Предпринимает ли юнит активные действия, или же смииренно принимает удары судьбы
        self.active = True
        self.last_direction = 9
        self.rich = 0
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        # draw
        pygame.draw.rect(self.image, color, [0, 0, self.width, self.height])
        # fetch
        # self.rect = self.image.get_rect()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # self.rect.x = self.x
        # self.rect.y = self.y
    def render(self):
        self.image = pygame.Surface([self.width, self.height])
        pygame.draw.rect(self.image, self.color, [0, 0, self.width, self.height])
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def __str__(self):
        return f'#################### {self.unitno} {self.family} ####################\n'+\
                f'Sex: {self.sex},\t Age: {round(int(self.age)/365, 2)}\tHealth: {round(self.health, 2)}\tStrength: {round(self.strength, 2)}\tAgression: {round(self.agression, 2)}\n'+\
                f'Rich {round(self.rich, 2)}, Child: {len(self.child)}, color: {self.color}\n'+\
                f'##################################################'
