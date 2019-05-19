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
    def __init__(self, xpos, ypos, color, width, height):
        # coding
        global unitno
        self.unitno = unitno
        unitno += 1
        self.x = xpos
        self.y = ypos
        self.width = width
        self.height = height
        self.color = color
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
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        # draw
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        # fetch
        self.rect = self.image.get_rect()

    def render(self):
        screen.blit(self.image, (self.x, self.y))

    def __str__(self):
        return f'Unit ID: {self.unitno}\nCurrent position: {self.x}, {self.y}\n'+\
                f'Sex: {self.sex},\t Age: {round(int(self.age)/365, 2)}\tHealth: {self.health}\n'+\
                f'Размер: {self.width}x{self.height}'
