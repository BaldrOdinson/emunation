# -*- coding: utf-8 -*-

import pygame
import numpy as np
from start_units import units_start_pul
from units_class import window, screen, info_string, map_x, map_y
from curr_pop_set import curr_pop_params
from units_age import unit_growing_up, unit_death
from unit_pregnancy import start_preg, childbirth
from units_relation import units_relations
from use_thread import ProcessingThread
from unit_businness import unit_food, unit_health_care, unit_legacy
import emu_settings

day_no = 0
units_list = []

# Класс юнитов задается в units_class

# шрифты
pygame.font.init()                              # Инициализация шрифтов
info_font = pygame.font.SysFont('Ubuntu', 12)

#Описания юнитов
units_list = units_start_pul()

# внешние переменные
food_price = 0
health_care = 100
gov_money = 0
# может быть short или long
# log_type = 'short'
# day_log_msg = 'На {day_no} день произошло: '

# ИГРОВОЙ ЦИКЛ
done = True                                     # Пока true игровой цикл отрабатывается
while done:
    emu_settings.day_log_msg = ''
    # обработчик событий
    for e in pygame.event.get():                # обработка списка событий игры, например для прерывания основного цикла
        if e.type == pygame.QUIT:
            done = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            m_down = pygame.mouse.get_pos()
            # print(f'Mouse {e.button}: {m[0]} {m[1]}')
            # По правой кнопке печатаем инфо о юните
            if e.button == 3:
                for unit in units_list:
                    if unit.x < m_down[0] < unit.x + unit.width:
                        # 30 - высота меню
                        if unit.y < m_down[1] - 30 < unit.y + unit.height:
                            print(unit)
        if e.type == pygame.MOUSEBUTTONUP:
            m_up = pygame.mouse.get_pos()
            # print(f'mouse window: ({m_down[0]}, {m_down[1]} : {m_up[0]}, {m_up[1]})')
            if e.button == 1:
                for unit in units_list:
                    if unit.x > m_down[0] and unit.x + unit.width < m_up[0]:
                        # 30 - высота меню
                        if unit.y > m_down[1] - 30 and unit.y + unit.height < m_up[1] - 30:
                            print(unit)




    # Действия
    day_no += 1
    emu_settings.day_no += 1
    dead_units = []
    born_units = []
    threads = []
    for unit in units_list:
        # возраст
        unit = unit_growing_up(unit)
        if unit_death(unit):
            dead_units.append(unit)
            # Наследство
            legacy_message, gov_money = unit_legacy(unit, units_list, gov_money)
        # беременность
        if unit.pregnancy:
            if unit.pregnancy_day < 275:
                unit.pregnancy_day +=1
            else:
                new_unit = childbirth(unit)
                born_units.append(new_unit)
        # питание
        unit = unit_food(unit, food_price)
        # медобслуживание
        unit, gov_money = unit_health_care(unit, health_care, gov_money)

        # столкновение юнитов (пересечения координат)
        # Проверяем для каждого юнита в списке активных
        if unit.active:
            unit.today_meeted_unit = []
            # действия при контакте
            # спиок действий в use_thread
            # потоки
            thread = ProcessingThread(unit, units_list, gov_money)
            threads.append(thread)

    # запускаем потоки обработки взаимодействий
    for thread in threads:
        thread.start()
    # Ждем завершения всех потоков
    for thread in threads:
        thread.join()

    # удаление умерших
    for unit in dead_units:
        units_list.remove(unit)
        print(f'-----xxx-----\n{unit.unitno} {unit.family} умер в возрасте {unit.age//365} лет, здоровье: {round(unit.health, 2)}, сила: {round(unit.strength, 2)}, ум: {round(unit.mind, 2)}, агрессия: {round(unit.agression, 2)}. '+\
                f'У него осталось {len(unit.child)} детей. {legacy_message}. Был путешественником на {unit.travaler}%, состояние {round(unit.rich, 2)}')
    # добавление рожденных
    for unit in born_units:
        units_list.append(unit)
        print(f'+++ Родился малыш {new_unit.unitno} {new_unit.family}, здоровье {new_unit.health}. Мама: {new_unit.mother.unitno} {new_unit.mother.family}, он ее {len(new_unit.mother.child)} ребенок. '+\
                f'Папа: {new_unit.father.unitno} {new_unit.father.family}, он его {len(new_unit.father.child)} ребенок. Путешественник на {unit.travaler}%')



    # Заливка
    screen.fill((50,50,50))                      # покраска холста в rgb
    info_string.fill((204, 102, 51))


    # Базовые параметры населения
    curr_pop_dict = curr_pop_params(units_list, day_no)

    # отрисовка объектов
    for unit in units_list:
        unit.render()

    # отрисовка шрифтов
    info_string.blit(info_font.render(f'Население: {curr_pop_dict["population_quant"]}', 1, (204, 204, 204)), (5, 0))
    info_string.blit(info_font.render(f'Беременных: {curr_pop_dict["pregnant"]}', 1, (204, 204, 204)), (5, 15))
    info_string.blit(info_font.render(f'Мужчин: {curr_pop_dict["males"]}', 1, (204, 204, 204)), (130, 0))
    info_string.blit(info_font.render(f'Женщин: {curr_pop_dict["females"]}', 1, (204, 204, 204)), (130, 15))
    info_string.blit(info_font.render(f'День: {day_no}', 1, (204, 204, 204)), (230, 0))
    info_string.blit(info_font.render(f'Год: {day_no//365}', 1, (204, 204, 204)), (230, 15))
    info_string.blit(info_font.render(f'Ср.ум: {curr_pop_dict["average_mind"]}', 1, (204, 204, 204)), (320, 15))
    info_string.blit(info_font.render(f'Ср.агрессия: {curr_pop_dict["average_agression"]}', 1, (204, 204, 204)), (320, 0))
    info_string.blit(info_font.render(f'Ср.возраст: {curr_pop_dict["average_age"]}', 1, (204, 204, 204)), (460, 0))
    info_string.blit(info_font.render(f'Ср.здоровье: {curr_pop_dict["average_health"]}', 1, (204, 204, 204)), (460, 15))
    info_string.blit(info_font.render(f'Деньги: {round(curr_pop_dict["money"], 2)}', 1, (204, 204, 204)), (580, 0))
    info_string.blit(info_font.render(f'Гос. казна: {round(gov_money, 2)}', 1, (204, 204, 204)), (580, 15))
    info_string.blit(info_font.render(f'$Еда: {round(curr_pop_dict["food_price"], 2)}', 1, (204, 204, 204)), (820, 0))
    # Отображение холста на экран
    window.blit(info_string, (0, 0))
    window.blit(screen, (0, 30))                 # начало отрисовки игрового экрана на холсте (30 - под сткорой состония)
    pygame.display.flip()                        # показ игрового окна, сцена

    # обновление переменных
    food_price = curr_pop_dict["food_price"]
    health_care = curr_pop_dict["health_care"]
    # pygame.time.delay(1)                         # задержка цикла 5 мс
    # Лог за день
    log_header = f'@@@@@@@   На {emu_settings.day_no} день произошло: '
    if emu_settings.day_log_msg:
        print(log_header + emu_settings.day_log_msg)
