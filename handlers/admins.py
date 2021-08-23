from asyncio.queues import QueueEmpty

from pyrogram import Client
from pyrogram.types import Message
from callsmusic import callsmusic

from config import BOT_NAME as BN
from helpers.filters import command, other_filters
from helpers.decorators import errors, authorized_users_only


@Client.on_message(command("pause") & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    if (
            message.chat.id not in callsmusic.pytgcalls.active_calls
    ) or (
            callsmusic.pytgcalls.active_calls[message.chat.id] == 'paused'
    ):
        await message.reply_text("𝙉𝙤 𝘼𝙣𝙮 𝙎𝙤𝙣𝙜 𝙋𝙡𝙖𝙮𝙞𝙣𝙜...")
    else:
        callsmusic.pytgcalls.pause_stream(message.chat.id)
        await message.reply_text("▶️ 𝙋𝙖𝙪𝙨𝙚𝙙.")


@Client.on_message(command("resume") & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    if (
            message.chat.id not in callsmusic.pytgcalls.active_calls
    ) or (
            callsmusic.pytgcalls.active_calls[message.chat.id] == 'playing'
    ):
        await message.reply_text("𝙉𝙤 𝘼𝙣𝙮 𝙎𝙤𝙣𝙜 𝙄𝙨 𝙋𝙖𝙪𝙨𝙚𝙙...")
    else:
        callsmusic.pytgcalls.resume_stream(message.chat.id)
        await message.reply_text("⏸ 𝙍𝙚𝙨𝙪𝙢𝙚𝙙.")


@Client.on_message(command("end") & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    if message.chat.id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("𝙉𝙤 𝘼𝙣𝙮 𝙎𝙤𝙣𝙜 𝙄𝙨 𝙎𝙩𝙧𝙚𝙖𝙢𝙞𝙣𝙜...")
    else:
        try:
            callsmusic.queues.clear(message.chat.id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(message.chat.id)
        await message.reply_text("❌ 𝙎𝙩𝙧𝙚𝙖𝙢𝙞𝙣𝙜 𝙎𝙩𝙤𝙥𝙥𝙚𝙙.")


@Client.on_message(command("skip") & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    if message.chat.id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("𝙉𝙤 𝘼𝙣𝙮 𝙎𝙤𝙣𝙜 𝙄𝙨 𝙋𝙡𝙖𝙮𝙞𝙣𝙜 𝙁𝙤𝙧 𝙎𝙠𝙞𝙥...")
    else:
        callsmusic.queues.task_done(message.chat.id)

        if callsmusic.queues.is_empty(message.chat.id):
            callsmusic.pytgcalls.leave_group_call(message.chat.id)
        else:
            callsmusic.pytgcalls.change_stream(
                message.chat.id,
                callsmusic.queues.get(message.chat.id)["file"]
            )

        await message.reply_text("➡️ 𝙎𝙤𝙣𝙜 𝙃𝙖𝙨 𝘽𝙚𝙚𝙣 𝙎𝙠𝙞𝙥𝙥𝙚𝙙.")
