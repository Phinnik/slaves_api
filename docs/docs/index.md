# Быстрый старт

## Большая просьба
Поставьте звездочку этой библиотеке. Это для меня многое значит.

Если у вас есть возможность контрибьютить, это тоже прекрасно!


## Установка
```
git clone https://github.com/Phinnik/slaves_api.git
pip install virtualenv
virtualenv venv
venv\Scripts\activate.bat
cd slaves_api
pip install -r requirements.txt
```

## Получение строки авторизации
1. Зайти в приложение [Рабы](https://vk.com/app7794757_434463725#/) через компьютер
1. Открыть панель разработчика
    * Google Chrome: клавиша F12
1. Перейти во вкладку 'Network'
1. Перезагрузить страницу (клавиша F5)
1. Во вкладке "XHR" окна "Network" нас интересует запрос с названием "start"
1. В разделе "Request Headers" этого запроса скопировать значение строки "authorization"
1. Вуаля, вы прекрасны. Это и есть строка авторизации.

## Использование
```
from slaves import Api
api = Api('YOUR AUTHORIZATION STRING') # Строка авторизации

print(f'Цена Павла Дурова: {api.user_get(1).price} р.')
# >>> Цена Павла Дурова: 28820753 р.
```

