from typing import List

from django.contrib import admin
from smsru.models import Log

from django.utils.translation import gettext as _

from smsru.service import SmsRuApi


def update_sms_status(model, request, queryset):
    api = SmsRuApi()
    for item in queryset:
        if item.sms_id:
            result, data = api.get_status(item.sms_id)
            if result:
                item.status = data['status']
                item.status_code = data['status_code']
                item.status_text = data['status_text']
                item.save()


update_sms_status.short_description = _("Update selected sms status")


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ['phone', 'sms_id', 'msg', 'status', 'status_text', 'created_at']
    date_hierarchy = 'created_at'
    actions = [update_sms_status]
