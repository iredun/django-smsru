from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from smsru.models import Log
from smsru.service import SmsRuApi


@csrf_exempt
def sms_callback(request):
    if request.method == 'POST':
        data = request.POST.getlist('data[]')
        hash = request.POST.get('hash')
        api = SmsRuApi()
        if api.validate_callback(data, hash):
            item = Log.objects.filter(sms_id=data[1]).first()
            item.status_code = data[2]
            item.save()
    return HttpResponse(100)
