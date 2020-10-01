from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.backends.smtp import EmailBackend
from django.utils.encoding import smart_str

from .models import Email


class DatabaseMixin:
    def write_db_messages(self, emails):
        messages = []

        for message in emails:
            messages.append(
                Email(
                    sender="%s" % message.from_email,
                    recipients=", ".join(message.recipients()),
                    subject="%s" % message.subject,
                    body="%s" % message.body,
                )
            )
        Email.objects.bulk_create(messages)

        return len(messages)


class EmailDatabaseBackend(DatabaseMixin, BaseEmailBackend):
    def send_messages(self, emails):
        self.write_db_messages(emails)


class EmailSmtpDatabaseBackend(DatabaseMixin, EmailBackend):
    def send_messages(self, emails):
        super().send_messages(emails)
        self.write_db_messages(emails)
