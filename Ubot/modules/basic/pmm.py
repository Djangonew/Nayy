
from pyrogram import filters, Client
from pyrogram.types import Message
from Ubot.core.db.permitdb import *
from . import *
from config import BOTLOG_CHATID, PM_LOGGER
from ubotlibs.ubot.utils import *



async def denied_users(filter, client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if not await pm_guard(chat_id, user_id):
        return False
    if message.chat.id in (await get_approved_users()):
        return False
    elif message.from_user.id == DEVS:

        return False

    else:
        return True


@Ubot("setlimit", cmds)
async def set_limit_cmd(client, message):
    user_id = message.from_user.id
    arg = get_arg(message)
    if not arg:
        await message.edit("`Gunakan format !setlimit angka`")
        return
    await set_limit(user_id, int(arg))
    await message.edit(f"**Limit disetel ke {arg}**")
    
@Ubot("setblock", cmds)
async def set_blocking_cmd(client, message):
    user_id = message.from_user.id
    arg = get_arg(message)
    if not arg:
        await message.edit("`Gunakan format !setblocking kata-kata`")
        return
    if arg == "default":
        await set_block_message(user_id, BLOCKED)
        await message.edit("**Pesan blokir diubah ke default**.")
        return
    await set_block_message(user_id, f"`{arg}`")
    await message.edit("**Pesan blokir disetel.**")


@Client.on_message(filters.command(["y", "ok", "a", "iya"], cmds) & filters.me & filters.private)
async def allow(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    pmpermit, pm_message, limit, block_message = await get_pm_settings(user_id)
    await allow_user(chat_id, user_id)
    await message.edit(f"**Menerima pesan dari [you](tg://user?id={chat_id}).**")
    async for message in client.search_messages(
        chat_id=message.chat.id, query=pm_message, limit=1, from_user="me"
    ):
        await message.delete()
    USERS_AND_WARNS[chat_id] = 0


@Client.on_message(filters.command(["no", "n", "tolak", "g"], cmds) & filters.me & filters.private)
async def deny(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    await deny_user(chat_id, user_id)
    await message.edit(f"**I have denied [you](tg://user?id={chat_id}) to PM me.**")



@Client.on_message(
    filters.private
    & filters.create(denied_users)
    & filters.incoming
    & ~filters.service
    & ~filters.me
    & ~filters.bot
    & ~filters.via_bot
)
async def reply_pm(client: Client, message):
    global FLOOD_CTRL
    user_id = message.from_user.id
    pmpermit, pm_message, limit, block_message = await get_pm_settings(user_id)
    user_warns = 0 if user_id not in USERS_AND_WARNS else USERS_AND_WARNS[user_id]
    tai = f"<b>📨 PESAN BARU</b>\n<b> • : </b>{message.from_user.mention}"
    tai += f"\n<b> • 👀 </b><a href='{message.link}'>Lihat Pesan</a>"
    tai += f"\n<b> • Message : </b><code>{message.text}</code>"
    await asyncio.sleep(0.1)
    if PM_LOGGER:
        await app.send_message(
                 BOTLOG_CHATID,
                 tai,
                 parse_mode=enums.ParseMode.HTML,
                 disable_web_page_preview=True)
    if pmpermit and user_warns <= limit - 2:
        user_warns += 1
        USERS_AND_WARNS.update({user_id: user_warns})
        if not FLOOD_CTRL > 0:
            FLOOD_CTRL += 1
        else:
            FLOOD_CTRL = 0
            return
        async for message in client.search_messages(
            chat_id=message.chat.id, query=pm_message, limit=1, from_user="me"
        ):
            await message.delete()
        await message.reply(pm_message, disable_web_page_preview=True)
        return
    await message.reply(block_message, disable_web_page_preview=True)
    await client.block_user(message.chat.id)
    USERS_AND_WARNS.update({user_id: 0})