import hashlib
import re
import requests

from django.conf import settings
from smsru.models import Log


class SmsRuApi:
    __api_id = None
    __login = None
    __password = None
    __is_test = 0
    __from = None
    __partner_id = None
    __api_url = 'https://sms.ru/sms/'
    __api_url_my = 'https://sms.ru/my/'

    def __init__(self):
        self._get_settings()

    def _get_settings(self):
        setting_key = 'SMS_RU'
        sms_ru = getattr(settings, setting_key, None)
        if sms_ru is None:
            raise KeyError(f"Key {setting_key} not found in settings.py")

        self.__api_id = sms_ru.get('API_ID', None)
        if self.__api_id is None:
            self.__login = sms_ru.get('LOGIN', None)
            self.__password = sms_ru.get('PASSWORD', None)
            if self.__login is None or self.__password is None:
                raise KeyError(f"LOGIN and PASSWORD not found in {setting_key}")

        self.__from = sms_ru.get('SENDER', None)
        self.__is_test = int(sms_ru.get('TEST', False))

    @staticmethod
    def beautify_phone(phone: str) -> str:
        return re.sub(r"\D", "", phone)

    def __request(self, url: str, post_param: dict) -> dict:
        if self.__api_id:
            post_param['api_id'] = self.__api_id
        else:
            post_param['login'] = self.__login
            post_param['password'] = self.__password

        post_param['json'] = 1

        if self.__from:
            post_param['from'] = self.__from
        if self.__partner_id:
            post_param['partner_id'] = self.__partner_id

        post_param['test'] = self.__is_test

        response = requests.post(url, data=post_param)

        data = response.json()

        return data

    def _sms_request(self, post_param: dict) -> dict:
        if 'to' in post_param:
            return_result = {k: False for k in post_param['to'].split(',')}
            phone_msg = {k: post_param['msg'] for k in post_param['to'].split(',')}
        else:
            return_result = {k: False for k, v in post_param['multi'].items()}
            phone_msg = post_param['multi']
            multi = post_param.pop('multi')
            for k, v in multi.items():
                post_param[f'multi[{k}]'] = v

        url = self.__api_url + 'send'
        data = self.__request(url, post_param)

        if isinstance(data, dict):
            if data['status'] == 'OK' and data['status_code'] == 100:
                for phone, result in data['sms'].items():
                    return_result[phone] = result['status_code'] == 100

                    itm = Log(
                        phone=phone,
                        status=result["status"],
                        msg=phone_msg.get(phone, None),
                        status_code=result["status_code"],
                        status_text=result.get("status_text", None),
                        sms_id=result.get("sms_id", None),
                        cost=result.get("cost", None),
                    )
                    itm.save()

        return return_result

    def send_one_sms(self, phone: str, msg: str) -> dict:
        phone_beautify = self.beautify_phone(phone)
        if phone_beautify:
            post_param = {
                'to': phone_beautify,
                'msg': msg
            }
            return self._sms_request(post_param)
        else:
            raise Exception(f'Bad phone number {phone_beautify}')

    def get_status(self, sms_id: str):
        post_param = {
            'sms_id': sms_id
        }
        url = self.__api_url + 'status'
        data = self.__request(url, post_param)

        if isinstance(data, dict):
            if data['status'] == 'OK' and data['status_code'] == 100:
                if sms_id in data['sms']:
                    return True, data['sms'][sms_id]
        return False, None

    def validate_callback(self, data: list, hash: str) -> bool:
        my_hash = self.__api_id + "".join(data)
        return hash == hashlib.sha256(my_hash.encode('utf-8')).hexdigest()

    def send_multi_sms(self, phone_sms: dict) -> dict:
        post_param = {
            "multi": dict()
        }
        for phone, msg in phone_sms.items():
            phone_beautify = self.beautify_phone(phone)
            if phone_beautify:
                post_param['multi'][phone_beautify] = msg

        return self._sms_request(post_param)

    def get_balance(self) -> float:
        url = self.__api_url_my + 'balance'
        data = self.__request(url, {})
        if data['status_code'] != 100:
            raise Exception(data['status_text'])
        
        return data['balance']

    def get_limit(self) -> dict:
        url = self.__api_url_my + 'limit'
        data = self.__request(url, {})
        if data['status_code'] != 100:
            raise Exception(data['status_text'])

        return {
            "total_limit": data['total_limit'],
            "used_today": data['used_today']
        }
