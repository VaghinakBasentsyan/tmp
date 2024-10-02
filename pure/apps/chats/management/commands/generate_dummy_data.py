import logging

from apps.chats.models import User, Chat
from apps.chats.utils import fetch_banner_image, send_banner_image

from django.conf import settings
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    USERS_COUNT = 1000
    CHATS_COUNT = 1000
    def handle(self, *args, **kwargs):
        user_names = [f"user_{i}" for i in range(self.USERS_COUNT)]
        existing_users = User.objects.filter(username__in=user_names).values_list('username', flat=True)
        non_existing_user_names = set(user_names) - set(existing_users)
        if not non_existing_user_names:
            return
        users = [
            User.objects.create_user(username=i) for i in non_existing_user_names
        ]
        Chat.objects.bulk_create([Chat(user=user) for user in users])
        for banner_data in fetch_banner_image(settings.API_URL):
            send_banner_image(banner_data)
