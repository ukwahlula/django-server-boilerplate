from django.core.management.base import BaseCommand

from apps.cms.models import Content
from apps.cms.presets import CONTENT_PRESETS


class Command(BaseCommand):
    help = "Initialize cms data from hardcoded presets"

    def handle(self, *args, **kwargs):
        for content_type, value in CONTENT_PRESETS.items():
            Content.objects.get_or_create(content_type=content_type, defaults=dict(content=value["content"]))
