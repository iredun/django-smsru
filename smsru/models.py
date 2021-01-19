from django.db import models
from django.utils.translation import gettext as _


class Log(models.Model):
    phone = models.CharField(verbose_name=_('Phone number'), max_length=30)
    msg = models.TextField(verbose_name=_('Message'))
    status = models.CharField(verbose_name=_('Status'), max_length=10)
    status_code = models.IntegerField(verbose_name=_('Status code'))
    status_text = models.TextField(verbose_name=_('Status text'), blank=True, null=True)
    sms_id = models.CharField(verbose_name=_('SMS ID'), max_length=255, blank=True, null=True)
    cost = models.FloatField(verbose_name=_('Cost'), blank=True, null=True)
    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Logs')
        verbose_name_plural = _('Log')
        ordering = ('-created_at', )
