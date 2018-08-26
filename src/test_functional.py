import os
import pytest
import allure
import drivers
import xml.etree.ElementTree as ET
from calcpage import CalcPage

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
SCENARIOS_XML = os.path.join(SCRIPT_DIR, 'test_funcitonal_scenarios.xml')

def get_scenarios(source):
    ''' Парсит источник со сценариями и возвращает кортеж вида (scanario_name, { arg_name:arg_value }) '''
    scenarios = ET.parse(source).getroot()
    scenarios = [ scenario.attrib for scenario in scenarios ]
    return scenarios

def pytest_generate_tests(metafunc):
    ''' (pytest test-generation feature) генерация сценариев по массиву кортежей из get_scenarios() '''
    idlist = []
    argvalues = []
    print('----------------')
    print('metafunc.cls.scenarios')
    for scenario in metafunc.cls.scenarios:
        idlist.append(scenario['name'])
        scenario.pop('name', None)
        items = scenario.items()
        argnames = [x[0] for x in items]
        argvalues.append(([x[1] for x in items]))
    metafunc.parametrize(argnames, argvalues, ids=idlist, scope="class")

class TestFunctional(object):
    scenarios = get_scenarios(SCENARIOS_XML)

    @allure.step('Установить сумму: {sum}')
    def step_set_sum(self, sum):
        if not sum: # для возможности создания сломанных тестов - т.е. тестов, которые падают не из-за ассерта
            raise Exception('Параметр sum обязателен для заполнения')
        self.calc.summa = sum

    @allure.step('Установить валюты ИЗ: {cur_from}')
    def step_set_currency_from(self, cur_from):
        self.calc.currency_from = cur_from

    @allure.step('Установить валюту В: {cur_to}')
    def step_set_currency_to(self, cur_to):
        self.calc.currency_to = cur_to

    @allure.step('Сконвертировать')
    def step_convert(self):
        return self.calc.convert()

    def setup_class(cls):
        cls.calc = CalcPage(drivers.chrome(), 'http://www.sberbank.ru/ru/quotes/converter').convertation_block

    def test_calc(self, sum, cur_from, cur_to, expect):
        ''' параметризированный тест правильность подсчета '''
        self.step_set_sum(sum)
        self.step_set_currency_from(cur_from)
        self.step_set_currency_to(cur_to)
        convertion_result = self.step_convert()
        assert convertion_result == expect

