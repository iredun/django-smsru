from django.core.management import BaseCommand
from smsru.service import SmsRuApi


class Command(BaseCommand):
    help = 'Send SMS'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--phone', dest='phone', default=None,
            help='Phone number',
        )
        parser.add_argument(
            '--msg', dest='msg', default=None,
            help='Message text',
        )

    def handle(self, *args, **options):
        phone = options.get('phone')
        msg = options.get('msg')

        api = SmsRuApi()
        result = api.send_one_sms(phone, msg)

        self.stdout.write(f"Result: {result}")
