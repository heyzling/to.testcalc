import pytest
import drivers
import re
from calcpage import CalcPage
from decimal import *

class Test_CalcPage():

    def setup_class(cls):
        cls.calc_page = CalcPage(drivers.chrome(), 'http://www.sberbank.ru/ru/quotes/converter')

    def test_title(self):
        assert self.calc_page.title == 'Калькулятор иностранных валют'

    def test_convertation_title(self):
        assert self.calc_page.convertation_block.title == 'Конвертация'

    @pytest.mark.order0
    def test_convert(self):
        convertation_result = self.calc_page.convertation_block.convert()
        assert re.match('\d{1,},\d{2}', convertation_result) is not None
        # assert convertation_result == Decimal('1.47') # курс меняется. Временная проверка.

    @pytest.mark.order1
    def test_convertation_get_summa(self):
        assert self.calc_page.convertation_block.summa == '100'

    @pytest.mark.run(after='test_convertation_get_summa')
    def test_convertation_set_summa(self):
        new_summa = 1234567
        self.calc_page.convertation_block.summa = new_summa
        assert self.calc_page.convertation_block.summa.replace(' ', '') == str(new_summa)

    @pytest.mark.order1
    def test_convertation_get_currency_from(self):
        assert self.calc_page.convertation_block.currency_from == 'RUB'

    @pytest.mark.run(after='test_convertation_get_currency_from')
    def test_convertation_set_currency_from(self):
        new_currency_from = 'CZK'
        self.calc_page.convertation_block.currency_from = new_currency_from
        assert self.calc_page.convertation_block.currency_from == new_currency_from

    @pytest.mark.order1
    def test_convertation_get_currency_to(self):
        assert self.calc_page.convertation_block.currency_to == 'USD'

    @pytest.mark.run(after='test_convertation_get_currency_to')
    def test_convertation_set_currency_to(self):
        new_currency_to = 'SGD'
        self.calc_page.convertation_block.currency_to = new_currency_to
        assert self.calc_page.convertation_block.currency_to == new_currency_to


if __name__ == '__main__':
    tst = Test_CalcPage()
    tst.setup_class()
    tst.test_convert()
    # tst.test_convertation_set_currency_from()
    # tst.test_convertation_set_currency_to()
    # Test_CalcPage().test_convertation_set_currency_to()
    # import time
    # page = CalcPage(drivers.chrome(False), 'http://www.sberbank.ru/ru/quotes/converter')
    # # # page.convertation_block.currency_from = 'USD'
    # # # page.convertation_block.currency_from = 'EUR'
    # # # page.convertation_block.currency_from = 'KZT'
    # # # page.convertation_block.currency_from = 'RUB'

    # page.convertation_block.currency_to = 'KZT'
