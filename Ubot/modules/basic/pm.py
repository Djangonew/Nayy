
import asyncio
from pyrogram.methods import messages
from pyrogram import filters, Client
from pyrogram.types import Message
from Ubot.core.db import permitdb as nay
from Ubot.core.db.permitdb import *


from . import *
from .pmm import denied_users, get_arg


@Ubot(["antipm"], cmds)
async def antipm(client, message):
    arg = get_arg(message)
    user_id = message.from_user.id
    if not arg:
        await message.edit("**Gunakan `on` untuk menghidupkan atau `off` untuk mematikan**")
        return
    if arg == "off":
        await set_pm(user_id, False)
        await message.edit("**Anti PM Off**")
    elif arg == "on":
        await set_pm(user_id, True)
        await message.edit("**Anti PM On**")
    else:
        await message.edit("**Gunakan `on` untuk menghidupkan atau `off` untuk mematikan**")


@Client.on_message(filters.command(["setpm"], cmds) & filters.me)
async def setpmmsg(client, message):
    arg = get_arg(message)
    user_id = message.from_user.id
    if not arg:
        await message.edit("**Mohon berikan pesan**")
        return
    if arg == "default":
        await nay.set_permit_message(user_id, nay.PMPERMIT_MESSAGE)
        await message.edit("**Pesan Anti PM Diset Default**.")
        return
    await nay.set_permit_message(user_id, f"`{arg}`")
    await message.edit("**Pesan Anti PM Diset**")
    

    

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