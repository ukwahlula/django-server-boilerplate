from django.template.loader import render_to_string

from apps.cms.models import Content

from .tasks import task_send_email


class Email:
    body_html = "email/body.html"

    def __init__(self, users, email_type_subject, email_type_body):
        self.users = users
        self.email_type_subject = email_type_subject
        self.email_type_body = email_type_body

    def render(self, user, attachments=None, context=None):
        subject = Content.objects.get_content(self.email_type_subject, context=context)
        body = Content.objects.get_content(self.email_type_body, context=context)
        body = render_to_string(self.body_html, {"body": body, "user_first_name": user.first_name})
        attachments = attachments or []
        return subject, body, attachments

    def send(self, attachments=None, context_func=None):
        email_data = {}
        for user in self.users:
            email_data[user.email.lower()] = self.render(
                user, attachments=attachments, context=context_func(user) if context_func else None
            )

        task_send_email.delay(email_data)
