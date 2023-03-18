import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import asyncio
import os
from gc import get_objects
import dotenv
from dotenv import load_dotenv
from os import environ, execle, path
from itertools import count

from pyrogram import Client, enums, filters
from pyrogram.types import *
from Ubot import CMD_HELP, StartTime, app, ids
from Ubot.core.db import *
from pyrogram.raw.functions import Ping
from Ubot.modules.bot.inline import get_readable_time
from . import *

load_dotenv()

session_counter = count(1)

    
@Client.on_message(filters.command("prem", cmds) & filters.me)
async def handle_grant_access(client: Client, message: Message):
    text = None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        text = message.text.split()
        if len(text) < 2:
            await message.reply_text("Maaf, format yang Anda berikan salah. Mohon balas ke pengguna atau berikan username/user ID.")
            return
        username = text[1]
        try:
            user = await client.get_users(username)
        except ValueError:
            user = None
        if user is None:
            await message.reply_text(f"Maaf, pengguna {username} tidak ditemukan.")
            return
        user_id = user.id

    if message.from_user.id not in ADMINS:
        await message.reply_text("Maaf, hanya admin yang dapat memberikan akses.")
        return

    duration = 1
    if text is not None and len(text) >= 3:
        try:
            duration = int(text[2])
        except ValueError:
            await message.reply_text("Maaf, format yang Anda berikan salah. Durasi harus dalam angka.")
            return

    await check_and_grant_user_access(user_id, duration)
    await message.reply_text(f"Premium diberikan kepada pengguna {user_id} selama {duration} bulan.")


@Client.on_message(filters.command("unprem", cmds) & filters.me)
async def handle_revoke_access(client: Client, message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        text = message.text.split()
        if len(text) < 2:
            await message.reply_text("Maaf, format yang Anda berikan salah. Mohon balas ke pengguna atau berikan username/user ID.")
            return
        username = text[1]
        try:
            user = await client.get_users(username)
        except ValueError:
            user = None
        if user is None:
            await message.reply_text(f"Maaf, pengguna {username} tidak ditemukan.")
            return
        user_id = user.id

    if message.from_user.id not in ADMINS:
        await message.reply_text("Maaf, hanya admin yang dapat mencabut akses.")
        return

    await delete_user_access(user_id)
    await message.reply_text(f"Akses dicabut untuk pengguna {user_id}.")