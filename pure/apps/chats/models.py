from apps.users.models import User

from django.db import models

class BaseTimedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Attachment(BaseTimedModel):
    #  in real life it would be with django-storages and boto3 to store data in s3
    external_id = models.IntegerField(null=True, blank=True, unique=True)
    title = models.CharField(max_length=255, null=True,  blank=True)
    description = models.TextField(null=True, blank=True)
    image_file = models.ImageField(upload_to='message_images/')
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"attachment: {self.id}"

class Chat(BaseTimedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Message(BaseTimedModel):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    message_text = models.TextField()
    attachment = models.ForeignKey(Attachment, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Message for {self.chat.user.username} at {self.created_at}"


