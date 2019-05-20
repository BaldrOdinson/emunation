# import numpy as np
from units_class import NationUnit, map_x, map_y
from random import randint

start_units_list = []

def one_nation_set(x, x_l, y, y_l, r_c_r, g_c_r, b_c_r, s_w, s_h, family, quantity):
    '''
    Формирование начального пула жителей, принадлежащих одной нации
    Координаты ареала обитания
    x - стартовая горизонталь на карте
    x_l - длина горизонтали
    y - стартовая вертикаль на карте
    y_l - длина вертикали
    Цвет жителя
    r_c_r - r_color_range - разброс по красному цвету (возможный оттенок красного)
    g_c_r - g_color_range - разброс по зеленому цвету (возможный оттенок зеленого)
    b_c_r - b_color_range - разброс по синему цвету (возможный оттенок синего)
    s_w - start_width - ширина значка жителя
    s_h - start_height - высота значка жителя
    family - собс-но фамилия группы индивидов
    quantity - количество жителей
    '''
    one_nation_list = []
    # ареал обитания
    start_x = x
    length_x = x_l
    start_y = y
    length_y = y_l
    # цвет юнитов
    r_color_range = r_c_r
    g_color_range = g_c_r
    b_color_range = b_c_r
    # размер юнитов
    start_width = s_w
    start_height = s_h
    # количество красных
    unit_quant = quantity
    for cur_num in range(0, quantity):
        cur_num_start_x = randint(start_x, start_x + length_x)
        cur_num_start_y = randint(start_y, start_y + length_y)
        color = (randint(r_color_range[0], r_color_range[1]), randint(g_color_range[0], g_color_range[1]), randint(b_color_range[0], b_color_range[1]))
        one_nation_list.append([cur_num_start_x, cur_num_start_y, color, start_width, start_height, family])
    return one_nation_list

# Красные, северо-запад
one_nation_list = one_nation_set(0, 300, 0, 300, (245, 255), (0, 10), (0, 10), 1, 1, 'Red', 15)
start_units_list += one_nation_list
# Синии, север
one_nation_list = one_nation_set(300, 300, 0, 300, (0, 10), (0, 10), (245, 255), 1, 1, 'Blue', 15)
start_units_list += one_nation_list
# Зеленый, северо-восток
one_nation_list = one_nation_set(600, 300, 0, 300, (0, 10), (245, 255), (0, 10), 1, 1, 'Green', 15)
start_units_list += one_nation_list
# Желтый, запад
one_nation_list = one_nation_set(0, 300, 300, 300, (245, 255), (245, 255), (0, 10), 1, 1, 'Yellow', 15)
start_units_list += one_nation_list
# Белый, центр
one_nation_list = one_nation_set(300, 300, 300, 300, (245, 255), (245, 255), (245, 255), 1, 1, 'White', 15)
start_units_list += one_nation_list
# Голубой, восток
one_nation_list = one_nation_set(600, 300, 300, 300, (0, 10), (245, 255), (245, 255), 1, 1, 'Cian', 15)
start_units_list += one_nation_list
# Фиолетовый, Юго-запад
one_nation_list = one_nation_set(0, 300, 600, 300, (245, 255), (0, 10), (245, 255), 1, 1, 'Violet', 15)
start_units_list += one_nation_list
# Черный, Юг
one_nation_list = one_nation_set(300, 300, 600, 300, (0, 10), (0, 10), (0, 10), 1, 1, 'Black', 15)
start_units_list += one_nation_list
# Серый, Юго-восток
one_nation_list = one_nation_set(600, 300, 600, 300, (122, 132), (122, 132), (122, 132), 1, 1, 'Gray', 15)
start_units_list += one_nation_list

# print (start_units_list)


# Создание юнитов, экземпляров класса NationUnit
def units_start_pul(start_units_list = start_units_list):
    units_list = []
    for unit in start_units_list:
        start_unit = NationUnit(xpos=unit[0], ypos=unit[1], color=unit[2], width=unit[3], height=unit[4], family=unit[5])
        units_list.append(start_unit)
    # Возраст
        start_unit.age = randint(7*365, 75*365)
    # Расчет размера
        size_coef = (start_unit.age + 3650)//3650
        start_unit.width = size_coef
        start_unit.height = size_coef
    # Здоровье
        start_unit.health = randint(90, 100)
        # print(f'\nСоздан новый юнит\n{start_unit}')
        start_unit.agression = randint(0, 100)
        start_unit.strength = randint(start_unit.age//365-10, start_unit.age//365+20)
        start_unit.mind = randint(0, 100)

    # Скорость перемещения
        if start_unit.age <= 18*365:
            start_unit.moving_coef = 1
        elif 18*365 < start_unit.age <= 40*365:
            start_unit.moving_coef = 3
        elif 40*365 < start_unit.age <= 60*365:
            start_unit.moving_coef = 2
        else:
            start_unit.moving_coef = 1

    # Тяга к путишествиям
        start_unit.travaler = randint(0, 100)
    return units_list
