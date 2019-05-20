import os
from threading import Thread
from unit_pregnancy import start_preg
from units_relation import units_relations
from unit_businness import unit_salary, unit_vacation
from units_moving import unit_move
import emu_settings

class ProcessingThread(Thread):
    '''
    Поток обработки событий одного из юнитов
    '''
    def __init__(self, unit, units_list, gov_money):
        Thread.__init__(self)
        self.unit = unit
        self.units_list = units_list
        self.day_no = emu_settings.day_no
        self.gov_money = gov_money

    def run(self):
        '''
        Запуск потока
        '''
        units_collide(self.unit, self.units_list, self.day_no)
        # перемещение
        unit = unit_move(self.unit)
        # работа
        unit = unit_salary(self.unit)
        # отдых
        unit_vacation(self.unit, self.gov_money)


# Просчет пересечения объектов
def Intersect(unit, other_unit):
    if (unit.x > other_unit.x - unit.width) and (unit.x < other_unit.x + other_unit.width) and \
        (unit.y > other_unit.y - unit.height) and (unit.y < other_unit.y + other_unit.height):
        unit.today_meeted_unit.append(other_unit)
        return 1
    else:
        return 0

# Что делать при контакте
def units_collide(unit, units_list, day_no):
    for other_unit in units_list:
        # если юнит из списка не текущий, не встречался и в списке соседей проверяем на пересечение
        if unit != other_unit and unit not in other_unit.today_meeted_unit:
            if Intersect(unit, other_unit) == True:
                # Действия при встрече
                if start_preg(unit, other_unit):
                    if emu_settings.log_type == 'short':
                        emu_settings.day_log_msg += 'P'
                    # print(f'У {unit.unitno} {unit.family} и {other_unit.unitno} {other_unit.family} будет малыш, уи-уи')
                unit, other_unit = units_relations(unit, other_unit)
                # print(f'На {day_no} день юнит {unit.unitno} встретил юнита {other_unit.unitno}')
            unit.today_meeted_unit.append(other_unit)
