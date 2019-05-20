import emu_settings

def units_relations(unit, other_unit):
    if (unit.agression <= 50 and other_unit.agression <= 50
        and unit.age >= 7*365 and other_unit.age >= 7*365):
        # если юниты не агрессивны, они могут поспорить
        unit, other_unit = units_dispute(unit, other_unit)
    if (unit.sex == other_unit.sex and
        (unit.agression > 50 or other_unit.agression > 50)
        and unit.age >= 18*365 and other_unit.age >= 18*365):
        unit, other_unit = units_fight(unit, other_unit)
    return unit, other_unit

# спор
def units_dispute(unit, other_unit):
    dispute_bet = unit.rich/100 + other_unit.rich/100
    unit.rich -= unit.rich/100
    other_unit.rich -= other_unit.rich/100
    if unit.mind > other_unit.mind:
        winner = f'Победил {unit.unitno} {unit.family}, ум: {round(unit.mind, 2)}/{round(other_unit.mind, 2)}.'
        unit.mind += 1
        if unit.agression >= 1:
            unit.agression -= 1
        other_unit.agression += 1
        # расчет
        unit.rich += dispute_bet
    elif unit.mind == other_unit.mind:
        winner = f'Ничья'
        unit.mind += 1
        other_unit.mind += 1
        if unit.agression >= 1:
            unit.agression -= 1
        if other_unit.agression >= 1:
            other_unit.agression -= 1
        #  расчет
        unit.rich += other_unit.rich/100
        other_unit.rich += unit.rich/100
    else:
        winner = f'Победил {other_unit.unitno} {other_unit.family}, ум: {round(other_unit.mind, 2)}/{round(unit.mind, 2)}.'
        other_unit.mind += 1
        if other_unit.agression >= 1:
            other_unit.agression -= 1
        unit.agression += 1
        # расчет
        other_unit.rich += dispute_bet
    # log
    if emu_settings.log_type == 'short':
        emu_settings.day_log_msg += 'D'
    elif emu_settings.log_type == 'long':
        emu_settings.day_log_msg += f'\n{unit.unitno} {unit.family} и {other_unit.unitno} {other_unit.family} поcпорили. {winner}'
    # print(f'На {day_no} день {unit.unitno} {unit.family} и {other_unit.unitno} {other_unit.family} поcпорили. {winner}')
    return unit, other_unit

# драка
def units_fight(unit, other_unit):
    fight_bet = unit.rich/10 + other_unit.rich/10
    unit.rich -= unit.rich/10
    other_unit.rich -= other_unit.rich/10
    if unit.strength > other_unit.strength:
        winner = f'Победил {unit.unitno} {unit.family}, сила: {round(unit.strength, 2)}/{round(other_unit.strength, 2)}, здоровье: {round(unit.health, 2)}/{round(other_unit.health, 2)}.'
        unit.strength += 1
        if unit.agression >= 1:
            unit.agression -= 1
        other_unit.agression += 1
        if other_unit.agression >= 50:
            other_unit.health -= 1*other_unit.agression/50
        else:
            other_unit.health -= 1
        # расчет
        unit.rich += fight_bet
    elif unit.strength == other_unit.strength:
        winner = f'Ничья'
        unit.strength += 1
        other_unit.strength += 1
        if unit.agression >= 1:
            unit.agression -= 1
        if other_unit.agression >= 1:
            other_unit.agression -= 1
        unit.health -= 1
        other_unit.health -= 1
        # расчет
        unit.rich += other_unit.rich/10
        other_unit.rich += unit.rich/10
    else:
        winner = f'Победил {other_unit.unitno} {other_unit.family}, сила: {round(other_unit.strength, 2)}/{round(unit.strength, 2)}, здоровье: {round(other_unit.health, 2)}/{round(unit.health, 2)}.'
        other_unit.strength += 1
        if other_unit.agression >= 1:
            other_unit.agression -= 1
        unit.agression += 1
        if unit.agression > 50:
            unit.health -= 1*unit.agression/50
        else:
            unit.health -= 1
        # расчет
        other_unit.rich += fight_bet
    # log
    if emu_settings.log_type == 'short':
        emu_settings.day_log_msg += 'F'
    elif emu_settings.log_type == 'long':
        emu_settings.day_log_msg += f'\n{unit.unitno} {unit.family} и {other_unit.unitno} {other_unit.family} подрались. {winner}'
    # print(f'На {day_no} день {unit.unitno} {unit.family} и {other_unit.unitno} {other_unit.family} подрались. {winner}')
    return unit, other_unit
