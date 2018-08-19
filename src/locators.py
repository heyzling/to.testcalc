from selenium.webdriver.common.by import By

class Locators():

    CONVERTATION_BLOCK = (By.CLASS_NAME, 'rates-aside__filter')
    CONVERTATION_BLOCK_TITLE = (By.CLASS_NAME, 'rates-aside__filter-title-text')
    CONVERTATION_BLOCK_SUMMA = (By.CSS_SELECTOR, 'input[placeholder="Сумма"]')
    CONVERTATION_BLOCK_CURRENCY_FROM = (By.CLASS_NAME, 'rates-aside__filter-block-line_field_converter-from')
    CONVERTATION_BLOCK_CURRENCY_TO = (By.CSS_SELECTOR, 'div.rates-aside__filter-block-line:nth-child(4)')