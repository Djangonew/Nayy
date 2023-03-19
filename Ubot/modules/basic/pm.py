
import asyncio
from pyrogram.methods import messages
from pyrogram import filters, Client
from pyrogram.types import Message
from Ubot.core.db.permit import *
from ubotlibs.ubot.helper.utility import get_arg
from . import *
from config import BOTLOG_CHATID, PM_LOGGER


FLOOD_CTRL = 0
ALLOWED = []
USERS_AND_WARNS = {}

async def denied_users(filter, client: Client, message: Message):
    if not await pm_guard():
        return False
    if message.chat.id in (await get_approved_users()):
        return False
    elif message.from_user.id == DEVS:
        return False
    else:
        return True


@Client.on_message(filters.command(["antipm"], cmds) & filters.me)
async def pmguard(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**Gunakan `on` untuk menghidupkan atau `off` untuk mematikan**")
        return
    if arg == "off":
        await set_pm(False)
        await message.edit("**Anti PM Off**")
    if arg == "on":
        await set_pm(True)
        await message.edit("**Anti PM On**")
        
@Client.on_message(filters.command(["setpm"], cmds) & filters.me)
async def setpmmsg(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**Mohon berikan pesan**")
        return
    if arg == "default":
        await set_permit_message(PMPERMIT_MESSAGE)
        await message.edit("**Pesan Anti PM Diset Default**.")
        return
    await set_permit_message(f"`{arg}`")
    await message.edit("**Pesan Anti PM Diset**")
    
@Client.on_message(filters.command(["setlimit"], cmds) & filters.me)
async def pmguard(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**Gunakan format angka**")
        return
    await set_limit(int(arg))
    await message.edit(f"**Limit diset {arg}**")



@Client.on_message(filters.command(["setblock"], cmds) & filters.me)
async def setpmmsg(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**Berikan pesan blokir**")
        return
    if arg == "default":
        await set_block_message(BLOCKED)
        await message.edit("**Block pesan diset default**.")
        return
    await set_block_message(f"`{arg}`")
    await message.edit("**Pesan Blokir Berhasil Diset**")


@Client.on_message(filters.command(["a", "ok"], cmds) & filters.me & filters.private)
async def allow(client, message):
    chat_id = message.chat.id
    pmpermit, pm_message, limit, block_message = await get_pm_settings()
    await allow_user(chat_id)
    await message.edit(f"**Menerima pesan dari [you](tg://user?id={chat_id}).**")
    async for message in client.search_messages(
        chat_id=message.chat.id, query=pm_message, limit=1, from_user="me"
    ):
        await message.delete()
    USERS_AND_WARNS.update({chat_id: 0})


@Client.on_message(filters.command(["no", "tolak"], cmds) & filters.me & filters.private)
async def deny(client, message):
    chat_id = message.chat.id
    await deny_user(chat_id)
    await message.edit(f"** [you](tg://user?id={chat_id}) DiTolak.**")

@Client.on_message(
    filters.private
    & filters.create(denied_users)
    & filters.incoming
    & ~filters.service
    & ~filters.me
    & ~filters.bot
    & ~filters.via_bot
)
async def reply_pm(app: Client, message):
    global FLOOD_CTRL
    pmpermit, pm_message, limit, block_message = await get_pm_settings()
    user = message.from_user.id
    user_warns = 0 if user not in USERS_AND_WARNS else USERS_AND_WARNS[user]
    user_id = message.from_user.id
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
    if user_warns <= limit - 2:
        user_warns += 1
        USERS_AND_WARNS.update({user: user_warns})
        if not FLOOD_CTRL > 0:
            FLOOD_CTRL += 1
        else:
            FLOOD_CTRL = 0
            return
        async for message in app.search_messages(
            chat_id=message.chat.id, query=pm_message, limit=1, from_user="me"
        ):
            await message.delete()
        await message.reply(pm_message, disable_web_page_preview=True)
        return
    await message.reply(block_message, disable_web_page_preview=True)
    await app.block_user(message.chat.id)
    USERS_AND_WARNS.update({user: 0})

add_command_help(
    "antipm",
    [
        [f"antipm [on or off]", " -> mengaktifkan dan menonaktifkan anti-pm."],
        [f"setpm [message or default]", " -> Sets a custom anti-pm message."],
        [f"setblock [message or default]", "-> Sets custom block message."],
        [f"setlimit [value]", " -> This one sets a max. message limit for unwanted PMs and when they go beyond it, bamm!."],
        [f"ok", " -> Allows a user to PM you."],
        [f"no", " -> Denies a user to PM you."],
    ],
)