# Django SMS.RU

[![PyPI version fury.io](https://badge.fury.io/py/django-smsru.svg)](https://pypi.org/project/django-smsru/)
[![PyPI license](https://img.shields.io/pypi/l/django-smsru.svg)](https://pypi.python.org/pypi/django-smsru/)

Приложение Django для быстрой интеграции API сервиса [sms.ru](https://sms.ru/?panel=api)

Быстрый старт
---------------

`pip install django-smsru`

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

Обязательно должен быть указан `API_ID` или пара `LOGIN` и `PASSWORD`, остальные параметры по желанию.

- `API_ID` - API ключ, если он указан, авторизация осуществляется только через него, Логин и Пароль при этом
  игнорируются
- `LOGIN` и `PASSWORD` - Логин и Пароль для авторизации запросов, используются только в случае если не указан `API_ID`
- `TEST` - отправлять ли сообщения в тестовом режиме, по умолчанию отправляем в нормальном режиме
- `SENDER` - имя отправителя
- `PARTNER_ID` - ID партнера

3. Добавьте в свой `urls.py` импорт URL (для работы callback, по желанию):

```
   path('smsru/', include('smsru.urls'))
```

4. Запустите ``python manage.py migrate`` для создания необходимых таблиц.

5. В админ панели вы сможете увидеть лог сообщений и запросить статус любого из них.

6. Так же добавилась консольная команда для отправки смс

```
python manage.py send-sms-ru --phone +79888888888 --msg Тест
```

# Сигналы
 - `smsru_call_back_sms(sender, instance, new_status)` - при обработке callback запроса, после изменения статуса сообщения

```python
from django.dispatch import receiver

from smsru.signals import smsru_call_back_sms


@receiver(smsru_call_back_sms)
def call_back_sms(sender, instance, new_status, *args, **kwargs):
    instance.msg = 'signal'
    instance.save()

```

# Использование библиотеки в коде

Отправка на один номер одного смс:

```python
from smsru.service import SmsRuApi

api = SmsRuApi()
result = api.send_one_sms("+79888888888", "Test")  # телефон и сообщение
# result: {'79888888888': True}
```

Отправка на множество номеров, разных сообщений:

```python
from smsru.service import SmsRuApi

api = SmsRuApi()
result = api.send_multi_sms({
    '+79888888888': 'test',
    '+79888888889': 'test 2',
})
# result: {'79888888888': True, '79888888889': True}
```

Получить баланс и лимиты:

```python
from smsru.service import SmsRuApi

api = SmsRuApi()
balance = api.get_balance()
limits = api.get_limit()
```