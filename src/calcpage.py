from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from locators import Locators
from base import Page
from base import Block
from tools import Actions

class CalcPage(Page):

    def __init__(self, driver, url):
        self._driver = driver
        self._url = url
        self._driver.get(url)
        
        # отключить назойливую плашку с сообщением о политике сборка Кук. Из-за нее едет весь скрипт
        policy_close = WebDriverWait(self._driver, 2).until(EC.presence_of_element_located(Locators.CLOSE_POLICY))
        actions = Actions(self._driver)
        actions.move_to_element(policy_close)
        actions.click()
        actions.perform()

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

    # ------- Методы для внутреннего использования. Должны возвращать WebElement
    def _get_el_title(self):
        ''' заголовок блок Конвертация'''
        return self._el.find_element(*Locators.CONVERTATION_BLOCK_TITLE)
    def _get_el_summa(self):
        ''' Поле для ввода суммы для конвертации'''
        return self._el.find_element(*Locators.CONVERTATION_BLOCK_SUMMA)
    def _get_el_currency_from(self):
        ''' списко с выбором валюты ИЗ которой надо конверитровать '''
        return self._el.find_element(*Locators.CONVERTATION_BLOCK_CURRENCY_FROM)
    def _get_el_currency_to(self):
        ''' списко с выбором валюты В которую надо конверитровать '''
        return self._el.find_element(*Locators.CONVERTATION_BLOCK_CURRENCY_TO)
    def _get_el_currency_item(self, currency_name):
        ''' Трехбуквенное имя валюты, которая расположена в списках ИЗ/В.  '''
        return WebDriverWait(self._driver, 2).until(
                lambda el: self._el.find_element(
                    By.XPATH, '//div[@class="visible"]/span[contains(text(), "{0}")]'.format(currency_name)),
                    message="Указанная валюта '{0}' не найдена. Проверьте, что список открыт, и что валюта в нем существует.".format(currency_name))

    # ------ Свойства для клиентского кода

    @property
    def title(self):
        ''' Текст заголовка блока '''
        return self._get_el_title().text

    @property
    def summa(self):
        ''' Сумма конвертации '''
        return self._get_el_summa().get_attribute('value')

    @summa.setter
    def summa(self, value):
        ''' Сумма конвертации '''
        summa_el = self._get_el_summa()
        summa_el.clear()
        summa_el.send_keys(str(value))

    @property
    def currency_from(self):
        ''' Валюта ИЗ которой происходит конвертация '''
        return self._get_el_currency_from().find_element(By.TAG_NAME, 'strong').text

    @currency_from.setter
    def currency_from(self, value):
        ''' Валюта ИЗ которой происходит конвертация '''
        self._get_el_currency_from().click()
        self._get_el_currency_item(value).click()

    @property
    def currency_to(self):
        ''' Целевая валюта В которую происходит конвертация '''
        return self._get_el_currency_to().find_element(By.TAG_NAME, 'strong').text

    @currency_to.setter
    def currency_to(self, value):
        ''' Целевая валюта В которую происходит конвертация '''
        self._get_el_currency_to().click()
        self._get_el_currency_item(value).click()
