from random import randint
from units_class import map_x, map_y

def unit_move(unit):
    '''
    Перемещение в рандомном направлении
    1 - N
    2 - N-O
    3 - O
    4 - S-O
    5 - S
    6 - S-W
    7 - W
    8 - N-W
    9 - No moving
    Скорость перемещения 1-2 клетки
    '''
    # Сохранение направления при достаточной тяге к приключениям
    if randint(0, 100) <= unit.travaler and unit.last_direction != 9:
        move_direction = unit.last_direction
    else:
        move_direction = randint(1, 9)
    unit.last_direction = move_direction
    speed = unit.moving_coef
    # N
    if move_direction == 1:
        if unit.y > 0:
            unit.y -= 1 * speed
        elif unit.y == 0:
            unit.y = map_y
    # N-O
    elif move_direction == 2:
        if unit.x < map_x:
            unit.x += 1 * speed
        elif unit.x == map_x:
            unit.x = 0
        if unit.y > 0:
            unit.y -= 1 * speed
        elif unit.y == 0:
            unit.y = map_y
    # O
    elif move_direction == 3:
        if unit.x < map_x:
            unit.x += 1 * speed
        elif unit.x == map_x:
            unit.x = 0
    # S-O
    elif move_direction == 4:
        if unit.x < map_x:
            unit.x += 1 * speed
        elif unit.x == map_x:
            unit.x = 0
        if unit.y < map_y:
            unit.y += 1 * speed
        elif unit.y == map_y:
            unit.y = 0
    # S
    elif move_direction == 5:
        if unit.y < map_y:
            unit.y += 1 * speed
        elif unit.y == map_y:
            unit.y = 0
    # S-W
    elif move_direction == 6:
        if unit.x > 0:
            unit.x -= 1 * speed
        elif unit.x == 0:
            unit.x = map_x
        if unit.y < map_y:
            unit.y += 1 * speed
        elif unit.y == map_y:
            unit.y = 0
    # W
    elif move_direction == 7:
        if unit.x > 0:
            unit.x -= 1 * speed
        elif unit.x == 0:
            unit.x = map_x
    # N-W
    elif move_direction == 8:
        if unit.x > 0:
            unit.x -= 1 * speed
        elif unit.x == 0:
            unit.x = map_x
        if unit.y > 0:
            unit.y -= 1 * speed
        elif unit.y == 0:
            unit.y = map_y
    # No unit_moving
    elif move_direction == 9:
        pass
    return unit
