from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from locators import Locators
from base import Page
from base import Block
from tools import Actions

class CalcPage(Page):

    @property
    def title(self):
        ''' Текста заголовка страницы '''
        return self._driver.find_element_by_css_selector('h1').text

    @property
    def convertation_block(self):
        ''' Блок конвертации валют '''
        return ConvertationBlock(self)



class ConvertationBlock(Block):
    ''' Блок конвертации валют. Главный управляющий блок приложения на странице. '''

    def __init__(self, parent_page):
        self._parent_page = parent_page
        self._driver = parent_page._driver
        self._el = WebDriverWait(self._driver, 5)\
            .until(lambda el: self._driver.find_element(*Locators.CONVERTATION_BLOCK))

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
    def currency_from(self, value):
        ''' Валюта из которой происходит конвертация '''
        cur_from_el = self.__get_el_currency_from()
        currency_el = cur_from_el.find_element(By.XPATH, '//span[contains(text(), "{0}")]'.format(value))
        actions = Actions(self._driver)
        actions \
            .move_to_element(cur_from_el) \
            .click() \
            .wait_until(EC.presence_of_element_located((By.CSS_SELECTOR, "div .visible")), expiration_time = 2) \
            .move_to_element(cur_from_el.find_element(By.XPATH, '//span[contains(text(), "{0}")]'.format(value))) \
            .click() \
            .wait_until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "{0}") and @class="selected"]'.format(value))), expiration_time = 1) \
            .perform()

    @property
    def currency_to(self):
        ''' Целевая валюта в которую происходит конвертация '''
        return self.__get_el_currency_to().find_element(By.TAG_NAME, 'strong').text

    @currency_to.setter
    def currency_to(self, value):
        ''' Целевая валюта в которую происходит конвертация '''

        # https://stackoverflow.com/questions/11908249/debugging-element-is-not-clickable-at-point-error
        cur_to_el = self.__get_el_currency_to()
        print(value)
        currency_el = cur_to_el.find_element(By.XPATH, '//span[contains(text(), "{0}")]'.format(value))
        print(currency_el.get_attribute('innerHTML'))


        actions = Actions(self._driver)
        actions \
            .move_to_element(cur_to_el) \
            .click() \
            .wait_until(EC.presence_of_element_located((By.CSS_SELECTOR, "div .visible")), expiration_time = 2) \
            .move_to_element(currency_el) \
            .perform()
        self._driver.execute_script("arguments[0].scrollIntoView()", cur_to_el.find_element(By.XPATH, '//span[contains(text(), "{0}")]'.format(value)))
        import time
        time.sleep(5)
        currency_el = WebDriverWait(self._driver, 5).until(lambda el: cur_to_el.find_element(By.XPATH, '//span[contains(text(), "{0}")]'.format(value)))
        currency_el.click()
        # actions = Actions(self._driver)
        # actions \
        #     .move_to_element(cur_to_el) \
        #     .click() \
        #     .wait_until(EC.presence_of_element_located((By.CSS_SELECTOR, "div .visible")), expiration_time = 2) \
        #     .move_to_element(cur_to_el.find_element(By.XPATH, '//span[contains(text(), "{0}")]'.format(value))) \
        #     .wait(1) \
        #     .click() \
        #     .perform()
        # .move_to_element(currency_el).click() \
            # .wait_until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "{0}") and @class="selected"]'.format(value))), expiration_time = 2) \

