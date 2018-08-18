from webdriver_manager.chrome import ChromeDriverManager

class CalcPage():

    def __init__(self, driver, url):
        self._driver = driver
        self._url = url
        self._driver.get(url)

        self.CalcBlock = Block(driver)

class Block():
    ''' обобщенный блок UI интерфейса '''

    def __init__(self, driver):
        self._driver = driver
