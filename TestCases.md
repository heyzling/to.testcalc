## Описание элементов и конвенция их именования

1. Блок **Калькулятор** - блок содержащий настройки конвертации
    1. Секция **Конвертация** - секция с полями **Сумма**, **Из**, **В**
    2. Радиокнопки **Источник** / **Получение** / ... - секция со списком значений из которых можно выбрать только одно.
    3. Кнопка **Показать**
    4. Секция **Вывод результата** - поазывает резльутат конвертации после нажати кнопки **Показать**.

2. Блок **Таблица котировок** - показывает таблицу (1 или 2 строки), в которой показаны текущие цены котировок для выбранной валютной пары

3. Блок **График котировок** - график с историей котировок для указанной валютной пары.

## Найденный функционал калькулятора

1. Если в секции **Конвертация** выбрать **Из** = "RUB", а второй любую другу валюту - val, в секции **Котировки** будет отображатся только одна строка - val/Rub
2. Если в секции **Конвертация** выбрать две любые валюты не RUB, то в секции **Котировки** будут отображаться две строки с котировкой каждой иностранной валюты относительно RUB.
3. Для некоторых валют нельзя выбрать чекбокс **Пакет услуг** (обнаружено на примере RUB/JPY)
4. В **Конвертации** при вводе в поле для ввода суммы отбрасываются все не числовые символы.
5. В **Конвертации** при вводе нуля кнопка **Показать** не работает (баг или фича?). **Поле результат** не изменяет свое занчение.
6. Если в Концвертации попытаться сделать одинаковыми две валюты, то происходит инверсия текущих валют (баг или фича?)
7. Если для валютной пары не стоят котировки, произвести расчет нельзя - кнопка **Показать** обнуляет текущий результат (если он есть). Нового результата не выводится.


## Сценарии тестирования

### Используемые переменные:

 - **CALC_URL** = http://www.sberbank.ru/ru/quotes/converter
 - **CUR1** - переменная для валюты №1
 - **CUR2** - переменная для валюты №2
 - **RUB** - валюта рубль

### Smoke

1. Страница загружается
   
   1. Открыть страницу по **CALC_URL**
   2. Проверить: Существует заголовок **Калькулятор иностранных валют**
   3. Проверить: Существует блок **Калькулятор**
   4. Проверить: Существует блок **Таблица изменения котировок**
   5. Проверить: Существует блок **Текущая котировка валютной пары**

2. Проверка первичной работоспособности калькулятора:
   
    1. Открыть страницу по **CALC_URL**
    2. В секции Конвертации в поле **Сумма** ввести значение 100.
    3. В секции Конвертация Выбрать **Из = RUB**, **В = USD**
    4. Нажать кнопку **Проверить**
    5. Проверить: секция **Вывод результата** содержит вывод формата *Вы получите: nn,nn RUB = nn,nn USD* (где nn - любые числа)
   
### UI

1. При выборе существующей валютной пары на основе рубля, пара отображаются в блоке **Таблица котировок**
   
    1. Открыть **CALC_URL**
    2. В блоке **Калькулятор** в секции **Конвертация** поставить значения, *ИЗ = **CUR1***, *В = **RUB***
    3. Проверить: в **Таблица котировок** одна запись
    4. Проверить: В первой строке **Таблица котировок** значения Валюта = **CUR1/RUB**
    5. Проверить: В первой строке **Таблица котировок** значения *Покупка* и *Продажа* содержат числа *nn,nn* (где n - цифра)

2. Выборе несуществующей валютной пары на основе рубля
   
    1. Открыть **CALC_URL**
    2. В блоке **Калькулятор** в секции **Конвертация** поставить значения, *ИЗ = RUB*, *В = PLN*
    3. Проверить: в блоке **Таблица котировок** значение в колонках **Покупка** и **Продажа** равны *-*

3. Проверить, что при выборе валютной пары без рубля, в таблице **Таблица котировок** отображается две записи - котировки этих валют в рублях.

 **TODO: тесты 1-3 можно обобщить, параметризировать и вынести написание таких тестов в отдельный конфиг (сборник сценариев)**

### Functional

Поиск ожидаемого результат.



1. Проверка подсчета RUB/USD на основании заранее известного результата.
   
    1. Открыть **CALC_URL**
    2. В блоке **Калькулятор** в секции **Конвертация** поставить значения *Сумма = 10000*, *ИЗ = RUB*, *В = USD*
    3. В блоке **Калькулятор** в секции **Время** поставить дату *21.01.2016*
    4. Нажать кнопку **Показать**
    5. Секция **Вывод результата** содержит строку равную *Вы получите: 10 000,00 RUB = 115,21 USD*

2. Проверка подсчета на основании текущих цен. Ожидаемые результат берется из источников на этом же сайте (например из **Таблицы котировок**)

3. 

4. Параметризация тестов