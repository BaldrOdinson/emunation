def curr_pop_params(units_list, day_no):
    '''
    Вычисление текущих параметров населения
    population_quant - Численность населения
    average_age - Средний возраст
    '''
    curr_pop_dict = {}
    # Численность
    curr_pop_dict['population_quant'] = len(units_list)
    average_age = 0
    average_health = 0
    average_mind= 0
    average_agression= 0
    health_care = 0
    pregnant = 0
    food_price = 0
    money = 0
    males = 0
    females = 0
    for unit in units_list:
        average_age += unit.age
        average_health += unit.health
        average_mind += unit.mind
        average_agression += unit.agression
        money += unit.rich
        food_price += unit.rich/100
        health_care += unit.rich/50
        if unit.sex == 'Male':
            males += 1
        else:
            females += 1
        if unit.pregnancy:
            pregnant += 1
    # Обработка параметров
    if curr_pop_dict['population_quant'] != 0:
        curr_pop_dict['average_age'] = round(average_age/curr_pop_dict['population_quant']/365, 2)
        curr_pop_dict['average_health'] = round(average_health/curr_pop_dict['population_quant'], 2)
        curr_pop_dict['average_mind'] = round(average_mind/curr_pop_dict['population_quant'], 2)
        curr_pop_dict['average_agression'] = round(average_agression/curr_pop_dict['population_quant'], 2)
        curr_pop_dict['food_price'] = round(food_price/curr_pop_dict['population_quant'], 2)
        curr_pop_dict['health_care'] = round(health_care/curr_pop_dict['population_quant'], 2)
        curr_pop_dict['males'] = males
        curr_pop_dict['females'] = females
        curr_pop_dict['pregnant'] = pregnant
        curr_pop_dict['money'] = money
    else:
        print('Конец. Все умерли. Протянули {day_no} дней.')

    return curr_pop_dict
