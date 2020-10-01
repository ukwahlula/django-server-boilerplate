import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage, get_connection

logger = logging.getLogger(__name__)


@shared_task
def task_send_email(email_data, connection=None):
    from_email = settings.DEFAULT_FROM_EMAIL

    connection = connection or get_connection(settings.EMAIL_BACKEND)

    for to in email_data:
        subject, body, attachments = email_data[to]
        msg = EmailMessage(subject, body, from_email, [to], reply_to=[to], connection=connection)

        msg.content_subtype = "html"

        for attachment in attachments:
            msg.attach_file(attachment)

        logger.info("Send email to %s", to)
        msg.send()
