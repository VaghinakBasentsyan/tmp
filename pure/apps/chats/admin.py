import uuid

from apps.chats.models import Chat, Message, Attachment
from apps.chats.utils import fetch_banner_image, send_banner_image

import httpx
from django.contrib import admin
from django.conf import settings
from django.db import transaction
from django.contrib import messages
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from django_admin_inline_paginator.admin import TabularInlinePaginated


#  I add pagination to prevent page crashes.
class MessageInline(TabularInlinePaginated):
    model = Message
    extra = 0
    fields = ()
    readonly_fields = ('display_image',)

    def display_image(self, instance):
        if instance.attachment.image_file:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />',
                               instance.attachment.image_file.url)
        return "No image"

    display_image.short_description = 'Image'

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    inlines = [MessageInline]
    search_fields = ('user__username',)
    list_filter = ('created_at',)
    actions = ['send_banner_to_all_chats']

    def changelist_view(self, request, extra_context=None):
        """
        Override changelist_view to allow action to be performed even if no items are selected.
        """
        if 'action' in request.POST and request.POST['action'] in self.actions:
            self.send_banner_to_all_chats(request, None)
            return HttpResponseRedirect(request.path)

        return super().changelist_view(request, extra_context=extra_context)

    @staticmethod
    def send_banner_to_all_chats(request, _=None):
        banner_image_data = next(fetch_banner_image(settings.API_URL), None)

        if not banner_image_data:
            messages.error(request, "No new unsent banner images available or there was an error fetching them.")
            return
        with transaction.atomic():
            send_banner_image(banner_image_data)
            messages.success(request, "Banner image sent to all chats successfully.")

    send_banner_to_all_chats.short_description = "Send unsent banner image to all chats"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'message_text', 'created_at')
    search_fields = ('chat__user__username', 'message_text')
    list_filter = ('created_at',)
    readonly_fields = ('display_image',)

    def display_image(self, instance):
        """
        Returns an HTML <img> tag for the attachment's image file.
        """
        if instance.attachment.image_file:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />',
                               instance.attachment.image_file.url)
        return "No image"

    display_image.short_description = 'Image'


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_file', 'created_at', 'display_image')
    list_filter = ('created_at',)

    def display_image(self, instance):
        """
        Returns an HTML <img> tag for the attachment's image file.
        """
        if instance.image_file:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />',
                               instance.image_file.url)
        return "No image"

    display_image.short_description = 'Image'
