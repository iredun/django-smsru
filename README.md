# Django SMS.RU


Приложение Django для быстрой интеграции API сервиса [sms.ru](https://sms.ru/?panel=api)

Быстрый старт
-----------

1. Добавьте `smsru` в INSTALLED_APPS:
```
   INSTALLED_APPS = [
     ...
     'smsru',
   ]
```
2. В настройках так же следует добавить параметр `SMS_RU`:
```
SMS_RU = {
    "API_ID": '<API KEY>', # если указан API ключ, логин и пароль пропускаем
    "LOGIN": '<login>', # если нет API, то авторизуемся чезер логин и пароль
    "PASSWORD": '<password>',
    "TEST": True, # отправка смс в тестовом режиме, по умолчанию False
    "SENDER": 'sms', # отправитель - необязательно поле
    "PARTNER_ID": 1111 # ID партнера - необязательно поле
}
```

3. Добавьте в свой `urls.py` импорт URL (для работы callback, по желанию):
```
   path('smsru/', include('smsru.urls'))
```

4. Запустите ``python manage.py migrate`` для создания необъодимых таблиц.

5. В админ панели вы сможете увидеть лог сообщений и запросить статус любого из них.

6. Так же добавилась консольная команда для отправки смс
```
python manage.py send-sms-ru --phone +79888888888 --msg Тест
```

# Использование библиотеки в коде
```python
from smsru.service import SmsRuApi
api = SmsRuApi()
result = api.send_one_sms("+79888888888", "Test") # телефон и сообщение
# result: {'79888888888': True}
```
