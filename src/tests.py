import drivers
from calcpage import CalcPage


class TestSuite_SberbankCalc():

    def test_one(self):
        pass


if __name__ == '__main__':
    
    calc = CalcPage(drivers.chrome(), 'http://www.sberbank.ru/ru/quotes/converter')
    # print(calc.title)
    # print(calc.convertation_block.title)
    # print(calc.convertation_block.summa)
    # calc.convertation_block.summa = 1234567
    # print(calc.convertation_block.summa)
    print(calc.convertation_block.currency_from)
    print(calc.convertation_block.currency_to)