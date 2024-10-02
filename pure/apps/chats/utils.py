import uuid
import logging

from apps.chats.models import Attachment, Message, Chat

import httpx
from django.core.files.base import ContentFile, File


logger = logging.getLogger(__name__)


def fetch_banner_image(api_url):
    try:
        response = httpx.get(api_url, timeout=30)
        data = response.raise_for_status().json()
        unsent_images = (img for img in data['photos'] if
                         not Attachment.objects.filter(external_id=img['id']).exists())
        yield from unsent_images

    except httpx.RequestError as e:
        logger.error(f"Error fetching banner image: {e}")
        return None

def send_banner_image(banner_image_data):
    response = httpx.get(banner_image_data['url'])
    response.raise_for_status()
    attachment = Attachment.objects.create(
        external_id=banner_image_data['id'],
        image_file=File(ContentFile(response.content), name=str(uuid.uuid4())),
        sent=False,
        title=banner_image_data['title'],
        description=banner_image_data['description'],
    )

    Message.objects.bulk_create(
        Message(
            chat=chat, attachment=attachment, message_text="Check out this banner!"
        ) for chat in Chat.objects.all()
    )
    attachment.sent = True
    attachment.save()
