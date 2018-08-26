import allure
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from locators import Locators
from tools import Actions

''' кол-во цифр после запятой у конвертируемых сумм '''
class CalcPage():

    def __init__(self, driver, url):
        self._driver = driver
        self._url = url
        self._driver.get(url)
        
        self.__el_convert = WebDriverWait(self._driver, 5)\
            .until(lambda el: self._driver.find_element(*Locators.CONVERTATION_BLOCK))

        # отключить назойливую плашку с сообщением о политике сборка Кук. Из-за нее едет весь скрипт
        policy_close = WebDriverWait(self._driver, 2).until(EC.presence_of_element_located(Locators.CLOSE_POLICY))
        self._driver.execute_script('arguments[0].click()', policy_close)
        WebDriverWait(self._driver, 2).until_not(EC.visibility_of_element_located(Locators.CLOSE_POLICY))

    # ------- Методы для внутреннего использования. Должны возвращать WebElement
    @property
    def _el_convert(self):
        ''' блок с настройками калькулятора - статический '''
        return self.__el_convert
    def _get_el_title(self):
        ''' заголовок блок Конвертация'''
        return self._el_convert.find_element(*Locators.CONVERTATION_BLOCK_TITLE)
    def _get_el_summa(self):
        ''' Поле для ввода суммы для конвертации'''
        return self._el_convert.find_element(*Locators.CONVERTATION_BLOCK_SUMMA)
    def _get_el_currency_from(self):
        ''' списко с выбором валюты ИЗ которой надо конверитровать '''
        return self._el_convert.find_element(*Locators.CONVERTATION_BLOCK_CURRENCY_FROM)
    def _get_el_currency_to(self):
        ''' списко с выбором валюты В которую надо конверитровать '''
        return self._el_convert.find_element(*Locators.CONVERTATION_BLOCK_CURRENCY_TO)
    def _get_el_currency_item(self, currency_name):
        ''' Трехбуквенное имя валюты, которая расположена в списках ИЗ/В.  '''
        return WebDriverWait(self._driver, 2).until(
                lambda el: self._el_convert.find_element(
                    By.XPATH, '//div[@class="visible"]/span[contains(text(), "{0}")]'.format(currency_name)),
                    message="Указанная валюта '{0}' не найдена. Проверьте, что список открыт, и что валюта в нем существует.".format(currency_name))
    def _get_el_show_button(self):
        ''' Кнопка Показать, которая запускает вычисления '''
        return self._el_convert.find_element(By.CLASS_NAME, 'rates-button')
    def _get_el_result_from(self):
        ''' результат конвертации - часть с суммой ИЗ которой конвертировали '''
        return WebDriverWait(self._driver, 2).until(
                lambda el: self._driver.find_element(*Locators.CONVERTATION_BLOC_RESULT_FROM),
                    message='Элемент не найден. Убедитесь, что была нажата кнопка Показать')
    def _get_el_result_to(self):
        ''' результат конвертации - часть с суммой В которую конвертировали '''
        return WebDriverWait(self._driver, 2).until(
                lambda el: self._driver.find_element(*Locators.CONVERTATION_BLOC_RESULT_TO),
                    message='Элемент не найден. Убедитесь, что была нажата кнопка Показать и что указанная пара валют котируется.')

    # ------ Свойства для клиентского кода

    @property
    def title(self):
        ''' Текста заголовка страницы '''
        return self._driver.find_element_by_css_selector('h1').text

    @property
    def summa(self):
        ''' Сумма конвертации '''
        return self.format_sum(self._get_el_summa().get_attribute('value'))

    @summa.setter
    @allure.step('Установить сумму: {value}')
    def summa(self, value):
        ''' Сумма конвертации '''
        if not value: # для возможности создания сломанных тестов - т.е. тестов, которые падают не из-за ассерта
            raise Exception('Сумма не может быть быт пустой строкой')
        summa_el = self._get_el_summa()
        summa_el.clear()
        summa_el.send_keys(str(value))

    @property
    def currency_from(self):
        ''' Валюта ИЗ которой происходит конвертация '''
        return self._get_el_currency_from().find_element(By.TAG_NAME, 'strong').text

    @currency_from.setter
    @allure.step('Установить валюту ИЗ: {value}')
    def currency_from(self, value):
        ''' Валюта ИЗ которой происходит конвертация '''
        self._get_el_currency_from().click()
        self._get_el_currency_item(value).click()

    @property
    def currency_to(self):
        ''' Целевая валюта В которую происходит конвертация '''
        return self._get_el_currency_to().find_element(By.TAG_NAME, 'strong').text

    @currency_to.setter
    @allure.step('Установить валюту В: {value}')
    def currency_to(self, value):
        ''' Целевая валюта В которую происходит конвертация '''
        self._get_el_currency_to().click()
        self._get_el_currency_item(value).click()

    @allure.step('Сконвертировать')
    def convert(self):
        ''' Нажимает кнопку Показать. Возвращает сконвертированную сумму '''
        self._get_el_show_button().click()
        summa = self.summa
        cur_from = self.currency_from
        WebDriverWait(self._driver, 2).until(
            EC.text_to_be_present_in_element(Locators.CONVERTATION_BLOC_RESULT_FROM, '{0} {1}'.format(summa, self.currency_from)))
        # проверка на ошибки при конвертации
        # TODO

        # возвращение результата - суммы конвертации
        convertation_result = self._get_el_result_to().text[:-4] # последние 4 символ - это пробел + код валюты
        return convertation_result

    def format_sum(self, sum):
        ''' Форматированние суммы. Для стандартизация. '''
        # калькулятор использует значения формата ddd,dd, но в поле ввода можно без них. Для стандартизации добавляю их сюда
        if ',' not in sum:
            sum += ',00'
        return sum


    