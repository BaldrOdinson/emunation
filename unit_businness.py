from random import randint
from math import trunc
from units_class import map_x, map_y
import emu_settings

def unit_salary(unit):
    '''
    расчет дневной выручки относительно текущих параметров юнита
    здоровье: 			70	70/100		0.7 	- уменьшение
    путешественник:		70	усидчивость 100-70=30/100					0.3 	- уменьшение
    ум:					150	20 min	150//20								7		- увеличение
    агрессия:			110	50 нейтрал	110/50	2,2						/2,2	- уменьшение
    богатство:			1000	20 начальный	1000/20		50			50		- увеличение
    дети:				4	1-4/10		0,6					            0,6		- уменьшение
    возраст:			3	коэф 2										2		- увеличение
					1 (7-18)	0,5
					2 (18-25)	1
					3 (25-35)	2
					4 (35-50)	3
					5 (50-60)	4
					6 (60-70)	2
					7 (70-85)	1
					8 (85-  )	0,5
    Base salary = 1
    '''
    base_day_slary = 1
    sal_health_coef = unit.health/100
    if unit.travaler == 100:
        sal_travel_coef = 1
    else:
        sal_travel_coef = (100 - unit.travaler)/100
    if unit.mind == 0:
        sal_mind_coef = 1/21
    else:
        sal_mind_coef = unit.mind/20
    if unit.agression <= 50:
        sal_agression_coef = 1
    else:
        sal_agression_coef = unit.agression/50
    # очень некоторые очень быстро богатеют
    # if unit.rich <= 2000:
    #     sal_rich_coef = 1
    # else:
    #     sal_rich_coef = unit.rich/2000
    sal_child_coef      = 1 - (len(unit.child)/10)
    # Возрастной коэфицент
    if 7*365 < unit.age <= 18*365:
        sal_age_coef = 0.5
    elif 18*365 < unit.age <= 25*365:
        sal_age_coef = 1
    elif 25*365 < unit.age <= 35*365:
        sal_age_coef = 2
    elif 35*365 < unit.age <= 50*365:
        sal_age_coef = 3
    elif 50*365 < unit.age <= 60*365:
        sal_age_coef = 4
    elif 60*365 < unit.age <= 70*365:
        sal_age_coef = 2
    elif 70*365 < unit.age <= 85*365:
        sal_age_coef = 1
    elif 85*365 < unit.age:
        sal_age_coef = 0.5

    # Дневной заработок:
    day_salary = (base_day_slary * sal_health_coef * sal_travel_coef
                * sal_mind_coef / sal_agression_coef * sal_child_coef)
                # * sal_rich_coef

    unit.rich += day_salary
    return unit

def unit_food(unit, food_price):
    # за еду плятят те кто работает
    if unit.age >= 7*365:
        if unit.rich >= food_price*100:
            unit.rich -= food_price
        else:
            unit.rich -= unit.rich/100
            unit.agression += 0.01
            if unit.agression > 50:
                unit.health -= 0.01 * unit.agression/50
    return unit

def unit_health_care(unit, health_care, gov_money):
    '''
    Определяем шанс и стоимость мед.обслуживания для улучшения здоровья
    '''
    # print(f'unit.rich: {unit.rich}, health_care: {health_care}')
    if health_care < 1:
        health_care = 1
    if unit.rich/50 < health_care or unit.rich/50 < 1:
        medicine_chance = 1
    else:
        # Чем юнит богаче, тем шанс выше
        medicine_chance = (unit.rich/50)//health_care
    # Стоимость 1 пункта лечения
    health_care_point_price = unit.rich/100
    # Если выпал шанс полечится
    curr_hospital_point = randint(1, 1000)
    # print(f'curr_hospital_point: {curr_hospital_point}, medicine_chance: {medicine_chance}')
    if curr_hospital_point <= medicine_chance:
        # Сколько пунктов будет залечено
        if unit.health < 99:
            h_c_point_available = randint(1, 100 - trunc(unit.health))
            unit.health += h_c_point_available
            # Оплата лечения
            h_c_price = h_c_point_available * health_care_point_price
            unit.rich -= h_c_price
            gov_money += h_c_price
            # LOGS
            if emu_settings.log_type == 'short':
                emu_settings.day_log_msg += 'H'
            elif emu_settings.log_type == 'long':
                emu_settings.day_log_msg += f'\n~~~ {unit.unitno} {unit.family} посетил больничку и подлечился на {h_c_point_available} за {round(h_c_price, 2)}. Теперь здоровье {round(unit.health, 2)}, а денег {round(unit.rich, 2)}'
    return unit, gov_money

def unit_vacation(unit, gov_money):
    '''
    Шанс для активного юнита отправиться в отпуск, для сброса агрессии
    Дальность поездки 1-450
    Стоимость 0.01 состояния за единицу сбрасываемой агрессии
    Сколько агресии сбрасывается определяется от 0 до 100 или текущей агресии, если она ниже
    '''
    agression_coef = 1 + unit.agression//50
    if randint(1, 1000//agression_coef) <= 1 and unit.agression > 50:
        vac_distance = randint(1, 450)
        if unit.agression < 100:
            agr_reset_max = trunc(unit.agression)
        else:
            agr_reset_max = 100
        agr_reset = randint(1, agr_reset_max)
        # расчет стоимости
        vac_cost = agr_reset * unit.rich/100
        # print(f'Агрессия до отпуска {unit.agression}')
        unit.agression -= agr_reset
        unit.rich -= vac_cost
        gov_money += vac_cost
        unit.x += vac_distance
        # перемещение, для смены обстановки, новые люди, места
        if unit.x > map_x:
            unit.x -=  map_x
        unit.y += vac_distance
        if unit.y > map_y:
            unit.y -=  map_y
        # LOGS
        if emu_settings.log_type == 'short':
            emu_settings.day_log_msg += 'V'
        elif emu_settings.log_type == 'long':
            emu_settings.day_log_msg += f'\n^^^ {unit.unitno} {unit.family} сгонял в отпуск. Сбросил {agr_reset} аргессии за {round(vac_cost, 2)}. Теперь агр: {round(unit.agression, 2)}, денег {round(unit.rich, 2)}'
    return unit, gov_money


def unit_legacy(dead_unit, units_list, gov_money):
    '''
    Расчет наследства.
    Состояние распределяется между детьми
    '''
    def legacy_spread(heirs, curr_legacy):
        '''
        Распределение оставшегося состояния
        '''
        heirs_num = len(heirs)
        if heirs_num > 0:
            heir_part = curr_legacy/heirs_num
            legacy_message = f'Наследство по {round(heir_part, 2)} получили: '
            for child_unit in heirs:
                legacy_message += f'{child_unit.unitno} {child_unit.family} '
                # rich_before = child_unit.rich
                child_unit.rich += heir_part
        return legacy_message

    curr_legacy = dead_unit.rich
    heirs = dead_unit.child
    family_heirs = []
    if len(heirs) > 0:
        # Наследникам - детям
        legacy_message = legacy_spread(heirs, curr_legacy)
    else:
        # Наследникам - семье
        # print(f'Наследство для юнита {child_unit.unitno}: до {rich_before}, после {child_unit.rich}')
        legacy_message = f'Наследников не обнаружено, деньги уходят членам семьи: '
        for unit in units_list:
            if dead_unit != unit and unit.family == dead_unit.family:
                family_heirs.append(unit)
        if len(family_heirs) > 0:
            legacy_fam_message = legacy_spread(family_heirs, curr_legacy)
            legacy_message += legacy_fam_message
        else:
            legacy_message = f'Наследников вообще нет, деньги уходят государству.'
            gov_money += curr_legacy
    return legacy_message, gov_money
