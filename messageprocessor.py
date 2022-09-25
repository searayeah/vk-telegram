from helper import set_keyboard_1


class MessageProcessor:
    def __init__(self, bot, vk_polling, tg_chat_id):
        self.bot = bot
        self.vk_polling = vk_polling
        self.tg_chat_id = tg_chat_id
        self.tab = "    "

        self.tg_prohibited_chars = [
            "_",
            "*",
            "[",
            "]",
            "(",
            ")",
            "~",
            "`",
            ">",
            "#",
            "+",
            "-",
            "=",
            "|",
            "{",
            "}",
            ".",
            "!",
        ]
        # self.message_types = ["user", "group", "chat"]
        self.parse_mode = "MarkdownV2"

        self.vk_message = None
        self.attachments = None
        self.conversation_name = None

        self.message_text = None
        self.answer = None

        self.conversation_active = None
        self.callback_data = None
        self.reply_markup = None

        # trailing stuff
        self.trailing = None
        self.tg_message_id = None
        self.peer_id_previous = None

        # talking to currently
        self.active_conversation_id = None
        self.active_conversation_name = None

    async def set(self, event):
        # TO-DO
        # кейс когда идет реплай на группу пересланных сообщений
        # message edit рассмотреть
        # 4096 UTF8 characters макс длина сообщения в телеге
        # если пригласили в беседу
        # если поменяли название беседы
        # стикер
        # attachments
        # fix text for \n and stuff
        # if youtube video is sent
        # if attachments number is more than one
        # скинули новость

        self.vk_message = (
            await self.vk_polling.api.messages.get_by_id(event.message_id)
        ).items[0]

        # self.attachments = await self.get_attachments(self.vk_message)

        # tg trailing message
        self.trailing = (
            self.trailing and self.peer_id_previous == self.vk_message.peer_id
        )

        if not self.trailing:
            self.conversation_name = f"_{await self.get_name(self.vk_message.peer_id)}_"
            self.answer = "Chat with: " + self.conversation_name

        self.message_text = await self.form_message(self.vk_message)
        self.answer += "\n" + self.message_text

        self.conversation_active = (
            self.active_conversation_id == self.vk_message.peer_id
        )
        self.callback_data = (
            f"answer.{self.vk_message.peer_id}.{self.conversation_name}"
        )
        self.reply_markup = (
            None
            if self.conversation_active
            else set_keyboard_1("Answer", self.callback_data)
        )

    async def send_msg(self):
        if self.trailing:
            await self.bot.edit_message_text(
                text=self.answer,
                chat_id=self.tg_chat_id,
                message_id=self.tg_message_id,
                parse_mode=self.parse_mode,
                reply_markup=self.reply_markup,
            )
        else:
            message = await self.bot.send_message(
                text=self.answer,
                chat_id=self.tg_chat_id,
                parse_mode=self.parse_mode,
                reply_markup=self.reply_markup,
            )
            self.tg_message_id = message.message_id
            self.peer_id_previous = self.vk_message.peer_id
            self.trailing = True

    async def form_message(self, message, level=0):
        text = await self.get_message_text(message, level)
        reply_message = await self.get_reply_message(message, level)
        forwarded_messages = await self.get_forwarded_messages(message, level)
        output = [text, reply_message, forwarded_messages]
        return "\n".join([x for x in output if x])

    async def get_message_text(self, message, level=0):
        name = await self.get_name(message.from_id)
        if message.text:
            return f"{self.set_tab(level)}*{name}*: {self.fix_text(message.text)}"
        else:
            return f"{self.set_tab(level)}*{name}*: Нет текста сообщения"

    async def get_reply_message(self, message, level=0):
        if message.reply_message:
            text = await self.get_message_text(message.reply_message, level + 1)
            return f"{self.set_tab(level)}_В ответ на:_\n{text}"
        else:
            return ""

    async def get_forwarded_messages(self, message, level=0):
        forwarded_messages_text = ""
        if message.fwd_messages:
            forwarded_messages_text += f"{self.set_tab(level)}_Пересланные сообщения_"
            for message in message.fwd_messages:
                forwarded_messages_text += "\n" + await self.form_message(
                    message, level + 1
                )
        return forwarded_messages_text

    def fix_text(self, text):
        if len(text) == 0:
            return "Ошибочка"  # а если фотография???))
        text = (
            text.replace("&lt;", "<")
            .replace("&gt;", ">")
            .replace("&quot;", '"')
            .replace("&amp;", "&")
        )
        for char in self.tg_prohibited_chars:
            text = text.replace(char, f"\\{char}")
        return text

    def get_message_type(self, peer_id):
        if peer_id < 0:
            return "group"
        elif peer_id > int(2e9):
            return "chat"
        else:
            return "user"

    async def get_name(self, peer_id):
        type = self.get_message_type(peer_id)
        if type == "group":
            group_info = await self.vk_polling.api.groups.get_by_id(abs(peer_id))
            return self.fix_text(group_info[0].name)
        elif type == "user":
            user_info = await self.vk_polling.api.users.get(peer_id)
            return self.fix_text(f"{user_info[0].first_name} {user_info[0].last_name}")
        elif type == "chat":
            chat_info = await self.vk_polling.api.messages.get_conversations_by_id(
                peer_id
            )
            return self.fix_text(chat_info.items[0].chat_settings.title)

    def set_tab(self, level):
        return self.tab * level

    def set_active_chat(self, callback_data):
        self.active_conversation_id = int(callback_data[1])
        self.active_conversation_name = callback_data[2]
        self.trailing = False

        output = {
            "text": f"Now talking with {self.active_conversation_name}",
            "parse_mode": self.parse_mode,
        }

        return output

    async def process(self, event):
        await self.set(event)
        await self.send_msg()
        print(self.__dict__)
