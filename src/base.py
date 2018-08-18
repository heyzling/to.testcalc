''' Базовые классы '''


class Page():
    ''' Образ страницы в виде объекта '''
    
    def __init__(self, driver, url):
        self._driver = driver
        self._url = url
        self._driver.get(url)

class Block():
    ''' обобщенный блок UI интерфейса '''

    def __init__(self, driver, locator):
        self._driver = driver
        # self._el = driver.find_element(locator)