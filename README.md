# to.testcalc

Тестовое задание по тестированию онлайн калькулятора валют от Сбербанка.

## Постановка

 - Придумать сценарии для тестирования Калькулятора иностранных валют на сайте http://www.sberbank.ru/ru/quotes/converter
 - Автоматизировать из них 3 сценария 

Результат выполненного ТЗ:

 - Реализовать функциональные (pytest) тесты сценариев.
 - Использовать инструмент Selenium WebDriver
 - Каждый тест должен выглядеть в отчете как отдельный тестовый сценарий
 - Тест должны быть параметризирован в XML или CSV
 - Результатом выполнения должен быть Yandex.Allure отчет
 - Исходный код проекта должен быть выложен на github или bitbucket.

## Описание проекта

NotImplemented ( =) )

### Yandex.Allure

Использованные фичи:

1. Степы - тесты пишутся с написанием шагов. Эти шаги (и результат их выполнения) можно посмотреть в отчете.

## Установка

Требования:

 - Python >= 3.6.5
 - pip >= 9.0.3
 - java >= 1.8.0_181-b13

```sh
git clone git@github.com:mirakulus/to.testcalc.git
cd to.testcalc
pip install -r requirements.txt
```

## Запуск

Указанная ниже последовательность комманд, запустит все тесты, сгенерирует и запустить в бразуере allure-отчет

```sh
cd to.testcalc
pytest --alluredir=reports
"allure/bin/allure" serve reports
```
