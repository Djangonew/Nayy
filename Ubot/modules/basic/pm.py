
import asyncio
from pyrogram.methods import messages
from pyrogram import filters, Client
from Ubot.core.db.permitdb import *
from Ubot.core.db import permitdb as nay
from . import *
from ubotlibs.ubot.utils import *
from .pmm import *

@Ubot("pmon", ".")
async def pmguard(client, message):
    user_id = message.from_user.id
    await nay.set_pm(user_id, True)
    await message.edit("**Antipm diaktifkan**")
        
@Ubot("pmoff", ".")
async def pmguard(client, message):
  user_id = message.from_user.id
  await nay.set_pm(user_id, False)
  await message.edit("**Antipm dimatikan**")
  

@Ubot("setpmmsg", ".")
async def set_pm_message_cmd(client, message):
    user_id = message.from_user.id
    arg = get_arg(message)
    if not arg:
        await message.edit("`Gunakan format !setpmmsg pesan`")
        return
    if arg == "default":
        await set_pm_message(user_id, PMPERMIT_MESSAGE)
        await message.edit("**Pesan Antipm diset ke default**.")
        return
    await set_pm_message(user_id, f"`{arg}`")
    await message.edit("**Pesan Antipm berhasil diubah.**")



add_command_help(
    "antipm",
    [
        [f"`pmon` or `pmoff`]", " -> mengaktifkan dan menonaktifkan anti-pm."],
        [f"setpm [message or default]", " -> Sets a custom anti-pm message."],
        [f"setblock [message or default]", "-> Sets custom block message."],
        [f"setlimit [value]", " -> This one sets a max. message limit for unwanted PMs and when they go beyond it, bamm!."],
        [f"ok, y atau a", " -> Allows a user to PM you."],
        [f"no, g atau n", " -> Denies a user to PM you."],
    ],
)