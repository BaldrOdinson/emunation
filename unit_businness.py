from random import randint
from math import trunc

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

def unit_health_care(unit, health_care, day_no):
    '''
    Определяем шанс и стоимость мед.обслуживания
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
    curr_hospital_point = randint(1, 300)
    # print(f'curr_hospital_point: {curr_hospital_point}, medicine_chance: {medicine_chance}')
    if curr_hospital_point <= medicine_chance:
        # Сколько пунктов будет залечено
        if unit.health < 99:
            h_c_point_available = randint(1, 100 - trunc(unit.health))
            unit.health += h_c_point_available
            # Оплата лечения
            h_c_price = h_c_point_available * health_care_point_price
            unit.rich -= h_c_price
            print(f'~~~ На {day_no} день {unit.unitno} посетил больничку и подлечился на {h_c_point_available} за {round(h_c_price, 2)}. Теперь здоровье {round(unit.health, 2)}, а денег {round(unit.rich, 2)}')
    return unit
