''' 
    Получить предустановленые инстансы драйверов. 
'''

import atexit
from selenium import webdriver


def chrome(set_headless = False, driver_path = None, quit_driver_at_exit = True):
    ''' Драйвер для бразуера Chrome
    set_headless - указывает, нужно ли запускать браузер в headless режиме (режим без отображения UI)
    driver_path - путь до драйвера. Если не указан, драйвер скачается автоматически.
    quit_driver_at_exit - автоматически закрыть сессию драйвера при окончании работы приложения (вызов driver.quit())
    '''
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager

    if not driver_path:
        driver_path = ChromeDriverManager().install()

    options = Options()
    options.set_headless(set_headless)

    # игнорировать ошибки серитфикатов и SSl. Иначе из-за этого периодически валятся тест с ошибкой
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    
    driver = webdriver.Chrome(executable_path=driver_path, options=options)

    if quit_driver_at_exit:
        atexit.register(driver.quit)

    return driver

def firefox(set_headless = False, driver_path = None, quit_driver_at_exit = True):
    ''' Драйвер для бразуера Firefox
    set_headless - указывает, нужно ли запускать браузер в headless режиме (режим без отображения UI)
    driver_path - путь до драйвера. Если не указан, драйвер скачается автоматически.
    quit_driver_at_exit - автоматически закрыть сессию драйвера при окончании работы приложения (вызов driver.quit())
    '''
    from selenium.webdriver.firefox.options import Options
    from webdriver_manager.firefox import GeckoDriverManager

    if not driver_path:
        driver_path = GeckoDriverManager().install()

    options = Options()
    options.set_headless(set_headless)
    
    driver = webdriver.Firefox(executable_path=driver_path, options=options)

    if quit_driver_at_exit:
        atexit.register(driver.quit)
        
    return driver

