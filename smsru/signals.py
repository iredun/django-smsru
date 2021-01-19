import django.dispatch

smsru_call_back_sms = django.dispatch.Signal(
    providing_args=["instance", "new_status"],
)
