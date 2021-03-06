import functools
import random
import uuid

from dumbot import Bot
from .text import get_all

rand64 = functools.partial(random.randrange, -2**63, 2**63)
seen = {}
bot = None


async def on_update(update):
    query = update.inline_query.query
    if not query:
        if update.message.chat.type == 'private':
            state = seen.get(update.message.chat.id)
            if not state:
                seen[update.message.chat.id] = 1
                await bot.sendMessage(
                    chat_id=update.message.chat.id,
                    text='I only work inline silly. Anyway, @Lonami made '
                         'me, and Richard hosts the server so thank him ❤️'
                )
            elif state == 1:
                seen[update.message.chat.id] = 2
                await bot.sendMessage(
                    chat_id=update.message.chat.id,
                    text="Hey, look, I don't have anything new to say."
                )
        return

    await bot.answerInlineQuery(
        inline_query_id=update.inline_query.id,
        results=[dict(
            type='article',
            id=str(uuid.uuid4()),
            title=title,
            input_message_content=dict(message_text=text)
        ) for title, text in get_all(query)]
    )
