from apps.cms.models import Content

from .tasks import task_send_sms


class Sms:
    def __init__(self, users, sms_type):
        self.users = users
        self.sms_type = sms_type

    def render(self, context=None):
        return Content.objects.get_content(self.sms_type, context=context)

    def send(self, context_func=None):
        sms_data = {}
        for user in self.users:
            sms_data[str(user.phone)] = self.render(context=context_func(user) if context_func else None)

        task_send_sms.delay(sms_data)


class SmsPhone:
    def __init__(self, phones, sms_type):
        self.phones = phones
        self.sms_type = sms_type

    def render(self, context=None):
        return Content.objects.get_content(self.sms_type, context=context)

    def send(self, context_func=None):
        sms_data = {}
        for phone in self.phones:
            sms_data[str(phone)] = self.render(context=context_func(phone) if context_func else None)

        task_send_sms.delay(sms_data)
