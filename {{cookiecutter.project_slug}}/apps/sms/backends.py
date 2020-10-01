from apps.sms.models import Sms


class SmsDatabaseBackend:
    def __init__(self, *args, **kwargs):
        pass

    def send(self, phone, sms):
        Sms.objects.create(phone=phone, sms=sms)
