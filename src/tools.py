''' '''

from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import time

class Actions(ActionChains):
    ''' расширение стандартного selenium.webdriver.ActionChains '''

    def wait_until(self, condition, expiration_time):
        ''' Ожидание выполнения условия. Аналог цепочки WebDriverWait(driver, 2).until(...)
        exporation_time - максимальное время ожидание (в секундах)
        condition - условие или ожидаемое событие. Может быть локатором в виде кортежа (By, query), лямбдой которая возвращает WebElement '''
        self._actions.append(lambda: WebDriverWait(self._driver, expiration_time).until(condition))
        return self

    def wait(self, seconds):
        ''' подождать указанное количество секунд '''
        self._actions.append(lambda: time.sleep(seconds))
        return self

