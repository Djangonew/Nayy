from pyrogram import Client, enums, filters
from pyrogram.types import *
from . import *
from ubotlibs.ubot.database import *
from ubotlibs.ubot.database.accesdb import *
from pyrogram.filters import chat
import asyncio
from typing import Dict, List, Union
from datetime import datetime, timedelta
from Ubot import BOTLOG_CHATID, app
from Ubot.modules.bot.start import log_tagged_messages

collection = cli["tag_log"]


async def idup_log(user_id: int, message: Message) -> bool:
    log = {"user_id": user_id}
    try:
        result = await collection.users.update_one(
            {'user_id': user_id},
            {'$set': {'tag_log': True}},
            upsert=True
        )
        if result.modified_count > 0 or result.upserted_id:
            await log_tagged_messages()
            return True
    except:
        return False


async def mati_log(user_id: int, message: Message) -> bool:
    log = {"user_id": user_id}
    try:
        result = await collection.users.update_one(
            {'user_id': user_id},
            {'$set': {'tag_log': False}},
            upsert=True
        )
        if result.modified_count > 0 or result.upserted_id:
            return False
    except:
        return False



@Client.on_message(filters.command("log", cmds) & filters.me)
async def set_log(client, message):
    user_id = message.from_user.id
    await idup_log(user_id, message)
    await message.edit("**Logger Tag Berhasil Dihidupkan**"
            )


@Client.on_message(filters.command("nolog", cmds) & filters.me)
async def set_no_log(client, message):
    user_id = message.from_user.id
    await mati_log(user_id, message)
    await message.edit("**Logger Tag Berhasil Dimatikan**"
            )
