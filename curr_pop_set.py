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
        if day_no%365 == 0:
            yearly_report(units_list, day_no)
    else:
        print(f'Конец. Все умерли. Протянули {day_no} дней.')

    return curr_pop_dict

def yearly_report(units_list, day_no):
    family_mem_count = {}
    family_rich_count = {}
    for unit in units_list:
        if unit.family in family_mem_count:
            family_mem_count[unit.family] += 1
        else:
            family_mem_count[unit.family] = 1
        if unit.family in family_rich_count:
            family_rich_count[unit.family] += unit.rich
        else:
            family_rich_count[unit.family] = unit.rich
    print(f'--------------- Годовой отчет за {day_no/365} год ---------------')
    for family, count in family_mem_count.items():
        print(f'В семье {family} \t{count} человек')
    print('~~~~~~~~~~~~~~      ~~~~~~~~~~~~~~      ~~~~~~~~~~~~~~')
    for family, richness in family_rich_count.items():
        print(f'Состояние семьи {family} \tсоставляет \t{round(richness, 2)}')
    print('-----------------------------------------------------------------')
