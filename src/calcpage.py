from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from locators import Locators
from base import Page
from base import Block

class CalcPage(Page):

    @property
    def title(self):
        ''' Текста заголовка страницы '''
        return self._driver.find_element_by_css_selector('h1').text

    @property
    def convertation_block(self):
        ''' Блок конвертации валют '''
        return ConvertationBlock(self._driver)



class ConvertationBlock(Block):
    ''' Блок конвертации валют. Главный управляющий блок приложения на странице. '''

    def __init__(self, driver):
        self._driver = driver
        self._el = driver.find_element(*Locators.CONVERTATION_BLOCK)

    def __get_el_title(self):
        return self._el.find_element(*Locators.CONVERTATION_BLOCK_TITLE)
    def __get_el_summa(self):
        return self._el.find_element(*Locators.CONVERTATION_BLOCK_SUMMA)
    def __get_el_currency_from(self):
        return self._el.find_element(*Locators.CONVERTATION_BLOCK_CURRENCY_FROM)
    def __get_el_currency_to(self):
        return self._el.find_element(*Locators.CONVERTATION_BLOCK_CURRENCY_TO)

    @property
    def title(self):
        ''' Текст заголовка блока '''
        return self.__get_el_title().text

    @property
    def summa(self):
        ''' Сумма конвертации '''
        return self.__get_el_summa().get_attribute('value')

    @summa.setter
    def summa(self, value):
        ''' Сумма конвертации '''
        summa_el = self.__get_el_summa()
        summa_el.clear()
        summa_el.send_keys(str(value))

    @property
    def currency_from(self):
        ''' Валюта из которой происходит конвертация '''
        return self.__get_el_currency_from().find_element(By.TAG_NAME, 'strong').text

    @currency_from.setter
    def currency_from(self):
        ''' Валюта из которой происходит конвертация '''
        raise Exception('not implemented')

    @property
    def currency_to(self):
        ''' Целевая валюта в которую происходит конвертация '''
        return self.__get_el_currency_to().find_element(By.TAG_NAME, 'strong').text

    @currency_to.setter
    def currency_to(self):
        ''' Целевая валюта в которую происходит конвертация '''
        raise Exception('not implemented')

