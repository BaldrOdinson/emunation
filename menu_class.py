# -*- coding: utf-8 -*-

import pygame, sys
from units_class import screen, info_string, window

class Menu:
    # x, y, Name, inactive color, active color, item_number
    def __init__(self, items = [50, 140, u'Item', (250, 250, 30), (250, 30, 250), 0]):
        self.items = items

    def render(self, poverhnost, font, num_item):
        for i in self.items:
            # Если выбранный пункт активный, то красим его в цвет активного, если нет, то в основной
            if num_item == i[5]:
                # i[0], i[1] - координаты пунктов, -30 по y из-за того что вверху отрисована закрашенная строка состояний,
                # и только под ней начинается экран меню со своими координатами
                poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], i[1]-30))
            else:
                poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], i[1]-30))

    def menu(self):
        done = True
        font_menu = pygame.font.Font('fonts/Ubuntu-L.ttf', 50)
        # деактивируем залипание клавиш
        pygame.key.set_repeat(0, 0)
        # курсор сделаем видимым
        pygame.mouse.set_visible(True)
        item = 0
        while done:
            # Красим и строку состояния и экран чтобы совпал размер
            info_string.fill((0, 100, 200))
            screen.fill((0, 100, 200))

            mp = pygame.mouse.get_pos()
            for i in self.items:
                if mp[0]>i[0] and mp[0]<i[0]+155 and mp[1]>i[1] and mp[1]<i[1]+50:
                    item = i[5]
            self.render(screen, font_menu, item)


            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        sys.exit()
                    # Навигация по меню с помощью клавиш
                    if e.key == pygame.K_UP:
                        if item > 0:
                            item -= 1
                    if e.key == pygame.K_DOWN:
                        if punkr < len(self.items) - 1:
                            item += 1
                # Навигация с помощью мыши
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    # Первый пункт - вход
                    if item == 0:
                        done = False
                    # Второй пункт - выход
                    if item == 1:
                        sys.exit()

            # Отображаем закрашенную в цвет меню строку состояний и экран меню
            window.blit(info_string, (0, 0))
            window.blit(screen, (0, 30))
            pygame.display.flip()
