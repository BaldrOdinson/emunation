from random import randint, choice
from units_class import NationUnit

def start_preg_unit(unit, father):
    unit.pregnancy = True
    unit.pregnancy_day = 1
    unit.child_father = []
    unit.child_father.append(father)

def start_preg(unit, other_unit):
    '''
    Проверяем подходят ли юниты для размножения и если да, то Female делаем беременной
    '''
    if unit.sex != other_unit.sex:
        # репродуктивный возраст от 18 до 50
        if (unit.age > 6570 and other_unit.age > 6570
            and unit.age < 18250 and other_unit.age < 18250):
            # Разница в возрасте не более 10 лет, в частности чтобы не налететь на семейное дело инцест
            if abs(unit.age - other_unit.age) <= 3650:
                # Здоровье не менее 50
                if unit.health > 50 and other_unit.health > 50:
                    if unit.sex == 'Female':
                        mother = unit
                        father = other_unit
                    else:
                        mother = other_unit
                        father = unit
                    # мать в данный момент не беременна и у нее, как и у отца, уже не более 5 детей
                    if not mother.pregnancy and len(mother.child) < 3 and len(father.child) < 3:
                        start_preg_unit(mother, father)
                        return True
    return False


def childbirth(unit):
    '''
    Роды нового юнита
    '''
    # Цвет ребенка
    mather_color = unit.color
    father_color = unit.child_father[-1].color
    child_color = ((mather_color[0]+father_color[0])//2, (mather_color[1]+father_color[1])//2, (mather_color[2]+father_color[2])//2)
    # Выставляем смещение по цветам +- 10, затем рандомом определяем точное значение
    # RED
    if child_color[0] - 10 <= 0:
        r_child_color_min = 0
    else:
        r_child_color_min = child_color[0] - 10
    if child_color[0] + 10 >= 255:
        r_child_color_max = 255
    else:
        r_child_color_max = child_color[0] + 10
    # GREEN
    if child_color[1] - 10 <= 0:
        g_child_color_min = 0
    else:
        g_child_color_min = child_color[1] - 10
    if child_color[1] + 10 >= 255:
        g_child_color_max = 255
    else:
        g_child_color_max = child_color[1] + 10
    # BLUE
    if child_color[2] - 10 <= 0:
        b_child_color_min = 0
    else:
        b_child_color_min = child_color[2] - 10
    if child_color[2] + 10 >= 255:
        b_child_color_max = 255
    else:
        b_child_color_max = child_color[2] + 10
    # Выставляем конечные цвета рандомном
    new_child_color = (randint(r_child_color_min, r_child_color_max),
                        randint(g_child_color_min, g_child_color_max),
                        randint(b_child_color_min, b_child_color_max))
    # 1% шанса мутации
    if randint(1, 100) <=1:
        mutation_color = choice(['r', 'g', 'b'])
        mutation_direction = int(choice(['0', '255']))
        if mutation_color == 'r':
            new_child_color[0] = mutation_direction
        elif mutation_color == 'g':
            new_child_color[1] = mutation_direction
        else:
            new_child_color[2] = mutation_direction
        print(f'Мутация: цвет {mutation_color} {mutation_direction} -> {new_child_color}')
    # Здоровье
    child_health = (unit.health + unit.child_father[-1].health)//2
    if child_health - 5 <= 0:
        child_health_min = 0
    else:
        child_health_min = child_health - 10
    if child_health + 15 >= 100:
        child_health_max = 100
    else:
        child_health_max = child_health + 10
    new_child_health = randint(child_health_min, child_health_max)
    # Тяга к путешествиям
    child_travaler = (unit.travaler + unit.child_father[-1].travaler)//2
    if child_travaler - 10 <= 0:
        child_travaler_min = 0
    else:
        child_travaler_min = child_travaler - 10
    if child_travaler + 10 >= 100:
        child_travaler_max = 100
    else:
        child_travaler_max = child_travaler + 10
    new_child_travaler = randint(child_travaler_min, child_travaler_max)

# Роды
    new_unit = NationUnit(xpos=unit.x+5, ypos=unit.y+5, color=new_child_color, width=1, height=1)
    new_unit.health = new_child_health
    new_unit.travaler = new_child_travaler
    new_unit.mother = unit
    new_unit.father = unit.child_father[-1]
    new_unit.family = unit.child_father[-1].family
    new_unit.age = 0
    new_unit.moving_coef = 0
    new_unit.agression = randint(0, 5)
    new_unit.strength = randint(0, (unit.strength+unit.child_father[-1].strength)//4)
    new_unit.mind = randint(0, (unit.mind+unit.child_father[-1].mind)//4)

    # Обнуление беременности
    unit.pregnancy = False
    unit.pregnancy_day = 0
    # Регистрация материнства и отцовства
    unit.child.append(new_unit)
    new_unit.father.child.append(new_unit)

    return new_unit
