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
    # xvel and yvel горизонтальная и вертикальная скорости.
    # при столкновении будем менять их вектор.
    # по идее должно будет меняться направление.
    # N
    if move_direction == 1:
        unit.yvel = -1
        if unit.rect.y > 0:
            unit.rect.y += unit.yvel * speed
        elif unit.rect.y <= 0:
            unit.rect.y = map_y
            # unit.rect.y -= unit.yvel * speed
    # N-O
    elif move_direction == 2:
        unit.xvel = 1
        unit.yvel = -1
        if unit.rect.x < map_x:
            unit.rect.x += unit.xvel * speed
        elif unit.rect.x >= map_x:
            unit.rect.x = 0
            # unit.rect.x += unit.xvel * speed
        if unit.rect.y > 0:
            unit.rect.y += unit.yvel * speed
        elif unit.rect.y <= 0:
            unit.rect.y = map_y
            # unit.rect.y -= unit.yvel * speed
    # O
    elif move_direction == 3:
        unit.xvel = 1
        if unit.rect.x < map_x:
            unit.rect.x += unit.xvel * speed
        elif unit.rect.x >= map_x:
            unit.rect.x = 0
            # unit.rect.x += unit.xvel * speed
    # S-O
    elif move_direction == 4:
        unit.xvel = 1
        unit.yvel = 1
        if unit.rect.x < map_x:
            unit.rect.x += unit.xvel * speed
        elif unit.rect.x >= map_x:
            unit.rect.x = 0
            # unit.rect.x += unit.xvel * speed
        if unit.rect.y < map_y:
            unit.rect.y += unit.yvel * speed
        elif unit.rect.y >= map_y:
            unit.rect.y = 0
            # unit.rect.y += unit.yvel * speed
    # S
    elif move_direction == 5:
        unit.yvel = 1
        if unit.rect.y < map_y:
            unit.rect.y += unit.yvel * speed
        elif unit.rect.y >= map_y:
            unit.rect.y = 0
            # unit.rect.y += unit.yvel * speed
    # S-W
    elif move_direction == 6:
        unit.xvel = -1
        unit.yvel = 1
        if unit.rect.x > 0:
            unit.rect.x += unit.xvel * speed
        elif unit.rect.x <= 0:
            unit.rect.x = map_x
            # unit.rect.x -= unit.xvel * speed
        if unit.rect.y < map_y:
            unit.rect.x += unit.xvel * speed
        elif unit.rect.y >= map_y:
            unit.rect.y = 0
            # unit.rect.x -= unit.xvel * speed
    # W
    elif move_direction == 7:
        unit.xvel = -1
        if unit.rect.x > 0:
            unit.rect.x += unit.xvel * speed
        elif unit.rect.x == 0:
            unit.rect.x = map_x
            # unit.rect.x -= unit.xvel * speed
    # N-W
    elif move_direction == 8:
        unit.xvel = -1
        unit.yvel = -1
        if unit.rect.x > 0:
            unit.rect.x += unit.xvel * speed
        elif unit.rect.x == 0:
            unit.rect.x = map_x
            # unit.rect.x -= unit.xvel * speed
        if unit.rect.y > 0:
            unit.rect.y += unit.yvel * speed
        elif unit.rect.y == 0:
            unit.rect.y = map_y
            # unit.rect.y -= unit.yvel * speed
    # No unit_moving
    elif move_direction == 9:
        pass
    return unit

def unit_rebound(unit):
    speed = unit.moving_coef
    unit.rect.x += unit.xvel * speed
    unit.rect.y += unit.yvel * speed
