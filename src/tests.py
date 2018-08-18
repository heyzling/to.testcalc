import drivers
from calcpage import CalcPage


class TestSuite_SberbankCalc():

    def test_one(self):
        pass


if __name__ == '__main__':
    calc = CalcPage(drivers.chrome(), 'http://www.sberbank.ru/ru/quotes/converter')