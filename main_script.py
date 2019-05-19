# -*- coding: utf-8 -*-

import pygame
import numpy as np
from start_units import units_start_pul
from units_class import window, screen, info_string, map_x, map_y
from curr_pop_set import curr_pop_params
from units_moving import unit_move
from units_age import unit_growing_up, unit_death
from unit_pregnancy import start_preg, childbirth
from units_relation import units_relations
from use_thread import ProcessingThread
from unit_businness import unit_salary, unit_food, unit_health_care

day_no = 0
units_list = []

# Класс юнитов задается в units_class

# шрифты
pygame.font.init()                              # Инициализация шрифтов
info_font = pygame.font.SysFont('Consolas', 14)

#Описания юнитов
units_list = units_start_pul()

# внешние переменные
food_price = 0
health_care = 100

# ИГРОВОЙ ЦИКЛ
done = True                                     # Пока true игровой цикл отрабатывается
while done:
    # обработчик событий
    for e in pygame.event.get():                # обработка списка событий игры, например для прерывания основного цикла
        if e.type == pygame.QUIT:
            done = False

    # Действия
    day_no += 1
    dead_units = []
    born_units = []
    for unit in units_list:
        # возраст
        unit = unit_growing_up(unit)
        # перемещение
        if unit.active:
            unit = unit_move(unit)
        # смерть
        if unit_death(unit):
            dead_units.append(unit)
        # беременность
        if unit.pregnancy:
            if unit.pregnancy_day < 275:
                unit.pregnancy_day +=1
            else:
                new_unit = childbirth(unit)
                born_units.append(new_unit)
        # заработок
        if unit.active:
            unit = unit_salary(unit)
        # питание
        unit = unit_food(unit, food_price)
        # медобслуживание
        unit = unit_health_care(unit, health_care, day_no)

    # удаление умерших
    for unit in dead_units:
        units_list.remove(unit)
        print(f'-xxx- Unit {unit.unitno} умер в возрасте {unit.age//365} лет, здоровье: {round(unit.health, 2)}, сила: {round(unit.strength, 2)}, ум: {round(unit.mind, 2)}, агрессия: {round(unit.agression, 2)}. '+\
                f'У него осталось {len(unit.child)} детей. Был путешественником на {unit.travaler}%, состояние {round(unit.rich, 2)}')
    # добавление рожденных
    for unit in born_units:
        units_list.append(unit)
        print(f'+++ Родился малыш, юнит {new_unit.unitno}, здоровье {new_unit.health}. Мама: {new_unit.mother.unitno}, он ее {len(new_unit.mother.child)} ребенок. '+\
                f'Папа: {new_unit.father.unitno}, он его {len(new_unit.father.child)} ребенок. Путешественник на {unit.travaler}%')


    # Заливка
    screen.fill((50,50,50))                      # покраска холста в rgb
    info_string.fill((204, 102, 51))


    # столкновение юнитов (пересечения координат)
    # Проверяем для каждого юнита в списке активных
    threads = []
    for unit in units_list:
        if unit.active:
            unit.today_meeted_unit = []
            # действия при контакте
            # спиок действий в use_thread
            # потоки
            thread = ProcessingThread(unit, units_list, day_no)
            threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # Базовые параметры населения
    curr_pop_dict = curr_pop_params(units_list, day_no)

    # отрисовка объектов
    for unit in units_list:
        unit.render()

    # отрисовка шрифтов
    info_string.blit(info_font.render(f'Население: {curr_pop_dict["population_quant"]}', 1, (204, 204, 204)), (5, 1))
    info_string.blit(info_font.render(f'Беременных: {curr_pop_dict["pregnant"]}', 1, (204, 204, 204)), (5, 15))
    info_string.blit(info_font.render(f'Мужчин: {curr_pop_dict["males"]}', 1, (204, 204, 204)), (130, 1))
    info_string.blit(info_font.render(f'Женщин: {curr_pop_dict["females"]}', 1, (204, 204, 204)), (130, 15))
    info_string.blit(info_font.render(f'День: {day_no}', 1, (204, 204, 204)), (230, 1))
    info_string.blit(info_font.render(f'Год: {day_no//365}', 1, (204, 204, 204)), (230, 15))
    info_string.blit(info_font.render(f'Ср.ум: {curr_pop_dict["average_mind"]}', 1, (204, 204, 204)), (330, 15))
    info_string.blit(info_font.render(f'Ср.агрессия: {curr_pop_dict["average_agression"]}', 1, (204, 204, 204)), (330, 1))
    info_string.blit(info_font.render(f'Ср.возраст: {curr_pop_dict["average_age"]}', 1, (204, 204, 204)), (500, 1))
    info_string.blit(info_font.render(f'Ср.здоровье: {curr_pop_dict["average_health"]}', 1, (204, 204, 204)), (500, 15))
    info_string.blit(info_font.render(f'Деньги: {round(curr_pop_dict["money"], 2)}', 1, (204, 204, 204)), (660, 1))
    info_string.blit(info_font.render(f'$Еда: {round(curr_pop_dict["food_price"], 2)}', 1, (204, 204, 204)), (660, 15))
    # Отображение холста на экран
    window.blit(info_string, (0, 0))
    window.blit(screen, (0, 30))                 # начало отрисовки игрового экрана на холсте (30 - под сткорой состония)
    pygame.display.flip()                        # показ игрового окна, сцена

    # обновление переменных
    food_price = curr_pop_dict["food_price"]
    health_care = curr_pop_dict["health_care"]
    # pygame.time.delay(1)                         # задержка цикла 5 мс
