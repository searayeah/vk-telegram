import asyncio
import logging
import os
from itertools import compress
from unittest.mock import call

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

from helper import set_keyboard_1, set_keyboard_8
from messageprocessor import MessageProcessor
from chatsprocessor import ChatsProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger = logging.getLogger(__name__)

TG_CHAT_ID = os.environ["TG_CHAT_ID"]
VK_TOKEN = os.environ["VK_TOKEN"]
TG_TOKEN = os.environ["TG_TOKEN"]

POLLING = UserPolling(api=API(VK_TOKEN))


async def run_polling(context):
    async for event in POLLING.listen():
        for update in event.get("updates", []):
            event = Event(update)  # IMPORTANT change vkbottle longpoll version to 3
            # vk_api Event class works only with ver 3 longpoll
            # while vkbottle uses default version 0
            if (
                event.type == VkEventType.MESSAGE_NEW  # and event.to_me
            ):  # for testing purposes
                logger.info(f"Entered new message")
                await context["message_processor"].process(event)


async def answer_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    callback_data = query.data.split(".", 2)  # if conv_name consists of some dots .

    if callback_data[0] == "answer":
        output = context.bot_data["message_processor"].set_active_chat(callback_data)
        message = await query.message.reply_text(**output)
        await message.pin()

    elif callback_data[0] == "chat":
        output = await context.bot_data["chats_processor"].set_chat_page(callback_data)
        await query.message.edit_text(**output)


async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.bot_data["message_processor"].active_conversation_id != None:
        await POLLING.api.messages.send(
            peer_id=context.bot_data["message_processor"].active_conversation_id,
            random_id=get_random_id(),
            message=update.message.text,
        )
    else:
        await update.message.reply_text(text="No chat selected")
    context.bot_data["message_processor"].trailing = False


async def now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TO-DO
    # if answer_name == none
    output = f"Now talking with {context.bot_data['message_processor'].active_conversation_name}"
    await update.message.reply_text(
        text=output, parse_mode=context.bot_data["message_processor"].parse_mode
    )
    context.bot_data["message_processor"].trailing = False


async def chats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    output = await context.bot_data["chats_processor"].set_chat_page()
    await update.message.reply_text(**output)
    context.bot_data["message_processor"].trailing = False


async def main():

    application = Application.builder().token(TG_TOKEN).build()

    application.add_handler(CommandHandler("now", now))
    application.add_handler(CommandHandler("chats", chats))

    application.add_handler(CallbackQueryHandler(answer_button))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, send_message)
    )

    application.bot_data["message_processor"] = MessageProcessor(
        application.bot, POLLING, TG_CHAT_ID
    )
    application.bot_data["chats_processor"] = ChatsProcessor(POLLING)
    async with application:

        await application.updater.start_polling()
        await application.start()

        # await test()
        await run_polling(context=application.bot_data)

        # run until it receives a stop signal
        await application.updater.stop()
        await application.stop()


asyncio.run(main())
