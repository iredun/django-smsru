from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from smsru.models import Log
from smsru.service import SmsRuApi
from smsru.signals import smsru_call_back_sms


@csrf_exempt
def sms_callback(request):
    if request.method == 'POST':
        data = [item[1][0].split('\n') for item in request.POST.lists() if 'data[' in item[0]]
        hash = request.POST.get('hash')
        api = SmsRuApi()
        if api.validate_callback(["\n".join(el) for el in data], hash):
            for data_item in data:
                item = Log.objects.filter(sms_id=data_item[1]).first()
                if item:
                    item.status_code = data_item[2]
                    item.save()
                    smsru_call_back_sms.send(item.__class__, instance=item, new_status=item.status_code)
    return HttpResponse(100)
