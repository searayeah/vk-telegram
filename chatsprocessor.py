
import asyncio
import logging
import os
from itertools import compress

import telegram
from telegram import (
    ForceReply,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from vk_api.longpoll import Event, VkEventType
from vk_api.utils import get_random_id
from vkbottle import API, UserPolling
from vkbottle.user import User
from vkbottle_types.objects import MessagesConversationPeerType

from helper import set_keyboard_1, set_keyboard_8, set_keyboard_7
from messageprocessor import MessageProcessor
from vkbottle_types.objects import MessagesConversationPeerType


class ChatsProcessor:
    def __init__(self, vk_polling):
        self.chats_count = None
        self.unread_count = None
        self.pages_number = None
        self.request_count = 6

        self.vk_polling = vk_polling

        self.page_turn = {"next": 1, "prev": -1}

    async def set_chat_page(self, callback_data=None):
        # если чатов меньше чем слотов в клаве, заполнить пропусками
        # добавить fix text
        # callback max 64 bytes
        # button text max 32 bytes
        page = 0
        reply_markup = None
        if callback_data:
            page = int(callback_data[1]) + self.page_turn[callback_data[2]]
        chats = await self.get_chats(page)

        if page == 0:
            reply_markup = set_keyboard_7(*chats, "Next", f"chat.{page}.next")
        elif page == self.pages_number:
            reply_markup = set_keyboard_7(*chats, "Prev", f"chat.{page}.prev")
        else:
            reply_markup = set_keyboard_8(
                *chats,
                "Prev",
                f"chat.{page}.prev",
                "Next",
                f"chat.{page}.next",
            )
        text = (
            f"Unread *{self.unread_count}* out of total of *{self.chats_count}*\n"
            + f"Page {page}/{self.pages_number}"
        )
        parse_mode = "MarkdownV2"  # вынести эти константы куда то отдельно
        output = {"text": text, "reply_markup": reply_markup, "parse_mode": parse_mode}
        return output

    async def get_chats(self, page):
        chats = await self.vk_polling.api.messages.get_conversations(
            count=self.request_count, extended=True, offset=page * self.request_count
        )

        self.unread_count = chats.unread_count
        self.chats_count = chats.count
        self.pages_number = chats.count // self.request_count + 1

        current_chats = []
        returned_chats_number = len(chats.items)
        for i in range(returned_chats_number):
            current_chats.extend(
                self.process_chat(chats.items[i], chats.profiles, chats.groups)
            )
        returned_diff = self.request_count - returned_chats_number
        current_chats.extend(["-", "-"] * (returned_diff))
        return current_chats

    def process_chat(self, chat, profiles, groups):
        name = ""
        unread_count = (
            f" ({chat.conversation.unread_count})"
            if chat.conversation.unread_count
            else ""
        )
        if chat.conversation.peer.type.value == "user":
            for profile in profiles:
                if profile.id == chat.conversation.peer.id:
                    name = f"{profile.first_name} {profile.last_name}"
        elif chat.conversation.peer.type.value == "group":
            for group in groups:
                if group.id == abs(chat.conversation.peer.id):
                    name = group.name
        elif chat.conversation.peer.type.value == "chat":
            name = chat.conversation.chat_settings.title
        callback_data = f"answer.{chat.conversation.peer.id}.{name}"
        return name + unread_count, callback_data
