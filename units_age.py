from random import randint, random
from pygame import Rect

def unit_growing_up(unit):
    '''
    взросление
    '''
    unit.age += 1
    # Возростная скорость передвижения
    if unit.age <= 6*365:
        unit.moving_coef = 0
        unit.active = False
    elif 6*365 < unit.age <= 18*365:
        if unit.active == False:
            unit.active = True
        unit.moving_coef = 1
    elif 18*365 < unit.age <= 40*365:
        unit.moving_coef = 3
    elif 40*365 < unit.age <= 60*365:
        unit.moving_coef = 2
    elif 60*365 < unit.age <= 80*365:
        unit.moving_coef = 1
    else:
        unit.moving_coef = 0
        unit.active = False
    # Возрастная сила
    if unit.age <= 50*365:
        unit.strength += 1/365
    elif 50*365 < unit.age <= 50*365:
        unit.strength -= 1/365/2
    else:
        unit.strength -= 1/365
    # Возрастное здоровье
    if unit.age > 60*365:
        unit.health -= 1/365
    # Возрастная сообразительность
    if unit.age <= 12*365:
        unit.mind += 1/365
    elif 12*365 < unit.age <= 25*365:
        unit.mind += 1.5/365
    elif 60*365< unit.age <= 80*365:
        unit.mind -= 1/365
    elif unit.age > 80*365:
        unit.mind -= 2/365
    #  Возрастной размер
    # Для половозрелых увеличим шанс встречи
    if 18*365 < unit.age < 50*365:
        size_coef = (unit.age + 365*2)// 3650
    else:
        size_coef = (unit.age + 365)// 3650
    unit.width = size_coef
    unit.height = size_coef
    unit.rect = Rect(unit.rect.x, unit.rect.y, unit.width, unit.height)
    return unit



def unit_death(unit):
    '''
    Безвременная кончина по естественным причинам
    Вероятности в день:
    '''
    full_ages = unit.age//365
    death_chance = random()
    # Здоровье. Плохое увеличивает шанс смерти
    if unit.health <= 0:
        return True
    health_coef = unit.health/100
    if unit.agression > 50:
        agression_coef = unit.agression/50
    else:
        agression_coef = 1

    if full_ages < 50:
        if unit.sex == 'Male':
            if death_chance <= 0.000009/health_coef*agression_coef:
                return True
        if unit.sex == 'Female':
            if death_chance <= 0.000007/health_coef*agression_coef:
                return True
    if 50 <= full_ages < 60:
        if unit.sex == 'Male':
            if death_chance <= 0.00001/health_coef*agression_coef:
                return True
        if unit.sex == 'Female':
            if death_chance <= 0.000009/health_coef*agression_coef:
                return True
    if 60 <= full_ages < 65:
        if unit.sex == 'Male':
            if death_chance <= 0.00003/health_coef*agression_coef:
                return True
        if unit.sex == 'Female':
            if death_chance <= 0.00001/health_coef*agression_coef:
                return True
    if 65 <= full_ages < 70:
        if unit.sex == 'Male':
            if death_chance <= 0.00005/health_coef*agression_coef:
                return True
        if unit.sex == 'Female':
            if death_chance <= 0.00003/health_coef*agression_coef:
                return True
    if 70 <= full_ages < 75:
        if unit.sex == 'Male':
            if death_chance <= 0.00007/health_coef*agression_coef:
                return True
        if unit.sex == 'Female':
            if death_chance <= 0.00005/health_coef*agression_coef:
                return True
    if 75 <= full_ages < 80:
        if unit.sex == 'Male':
            if death_chance <= 0.00009/health_coef*agression_coef:
                return True
        if unit.sex == 'Female':
            if death_chance <= 0.00007/health_coef*agression_coef:
                return True
    if 80 <= full_ages < 85:
        if unit.sex == 'Male':
            if death_chance <= 0.0001/health_coef*agression_coef:
                return True
        if unit.sex == 'Female':
            if death_chance <= 0.00009/health_coef*agression_coef:
                return True
    if 85 <= full_ages < 90:
        if unit.sex == 'Male':
            if death_chance <= 0.0003/health_coef*agression_coef:
                return True
        if unit.sex == 'Female':
            if death_chance <= 0.0001/health_coef*agression_coef:
                return True
    if 90 <= full_ages < 95:
        if unit.sex == 'Male':
            if death_chance <= 0.0005/health_coef*agression_coef:
                return True
        if unit.sex == 'Female':
            if death_chance <= 0.0003/health_coef*agression_coef:
                return True
    if 95 <= full_ages < 100:
        if unit.sex == 'Male':
            if death_chance <= 0.0007/health_coef*agression_coef:
                return True
        if unit.sex == 'Female':
            if death_chance <= 0.0005/health_coef*agression_coef:
                return True
    if full_ages >= 100:
        if unit.sex == 'Male':
            if death_chance <= 0.0009/health_coef*agression_coef:
                return True
        if unit.sex == 'Female':
            if death_chance <= 0.0007/health_coef*agression_coef:
                return True
