from django.urls import path

from smsru.views import sms_callback

app_name = 'smsru'

urlpatterns = [
    path('callback/sms/', sms_callback)
]
