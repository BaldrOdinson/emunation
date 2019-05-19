def units_relations(unit, other_unit, day_no):
    if (unit.agression <= 50 and other_unit.agression <= 50
        and unit.age >= 7*365 and other_unit.age >= 7*365):
        # если юниты не агрессивны, они могут поспорить
        unit, other_unit = units_dispute(unit, other_unit, day_no)
    if (unit.sex == other_unit.sex and
        (unit.agression > 50 or other_unit.agression > 50)
        and unit.age >= 18*365 and other_unit.age >= 18*365):
        unit, other_unit = units_fight(unit, other_unit, day_no)
    return unit, other_unit

# спор
def units_dispute(unit, other_unit, day_no):
    if unit.mind > other_unit.mind:
        winner = f'Победил {unit.unitno}, ум: {round(unit.mind, 2)}/{round(other_unit.mind, 2)}.'
        unit.mind += 1
        if unit.agression >= 1:
            unit.agression -= 1
        other_unit.agression += 1
    elif unit.mind == other_unit.mind:
        winner = f'Ничья'
        unit.mind += 1
        other_unit.mind += 1
        if unit.agression >= 1:
            unit.agression -= 1
        if other_unit.agression >= 1:
            other_unit.agression -= 1
    else:
        winner = f'Победил {other_unit.unitno}, ум: {round(other_unit.mind, 2)}/{round(unit.mind, 2)}.'
        other_unit.mind += 1
        if other_unit.agression >= 1:
            other_unit.agression -= 1
        unit.agression += 1
    # print(f'На {day_no} день {unit.unitno} и {other_unit.unitno} поcпорили. {winner}')
    return unit, other_unit

# драка
def units_fight(unit, other_unit, day_no):
    if unit.strength > other_unit.strength:
        winner = f'Победил {unit.unitno}, сила: {round(unit.strength, 2)}/{round(other_unit.strength, 2)}, здоровье: {round(unit.health, 2)}/{round(other_unit.health, 2)}.'
        unit.strength += 1
        if unit.agression >= 1:
            unit.agression -= 1
        other_unit.agression += 1
        if other_unit.agression >= 50:
            other_unit.health -= 1*other_unit.agression/50
        else:
            other_unit.health -= 1
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
    else:
        winner = f'Победил {other_unit.unitno}, сила: {round(other_unit.strength, 2)}/{round(unit.strength, 2)}, здоровье: {round(other_unit.health, 2)}/{round(unit.health, 2)}.'
        other_unit.strength += 1
        if other_unit.agression >= 1:
            other_unit.agression -= 1
        unit.agression += 1
        if unit.agression > 50:
            unit.health -= 1*unit.agression/50
        else:
            unit.health -= 1
    # print(f'На {day_no} день {unit.unitno} и {other_unit.unitno} подрались. {winner}')
    return unit, other_unit
