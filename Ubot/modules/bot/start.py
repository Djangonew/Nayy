
import heroku3
import time
import re
import asyncio
import math
import shutil
import sys
import dotenv
import datetime
from dotenv import load_dotenv
from os import environ, execle, path
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from Ubot.core.db import *
from Ubot import *
from itertools import count
from Ubot.modules.basic import *
from ubotlibs.ubot import Ubot, Devs
from pyrogram import *
from platform import python_version as py
from pyrogram import __version__ as pyro
from pyrogram.types import * 
from io import BytesIO

from Ubot.logging import LOGGER
from config import SUPPORT

def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "Ubot"])

HAPP = None

load_dotenv()

session_counter = count(1)

ANU = """
❏ **Users** Ke {}
├╼ **Nama**: {}
╰╼ **ID**: {}
"""

command_filter = filters.private & filters.command("buat") & ~filters.via_bot        
@app.on_message(command_filter)
async def create_env(client, message):
    filename = ".env"
    client = pymongo.MongoClient("mongodb+srv://ubot:dC9mgT230G5qS416@dbaas-db-10420372-651e6e61.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=dbaas-db-10420372")
    db = client["telegram_sessions"]
    mongo_collection = db["sesi_collection"]
    user_id = mongo_collection.find_one({"user_id": message.chat.id})
    cek = db.command("collstats", "sesi_collection")["count"]
    mongo_collection = db["sesi_collection"] 
    if not user_id:
        await message.reply_text("Session stringgnya belum ada nih, coba klik /string")
    else:
        sesi = user_id.get('session_string')
        filename = ".env"
        if os.path.isfile(filename):
            with open(filename, "r") as file:
                contents = file.read()
                if sesi in contents:
                    await message.reply_text(f"Session sudah tersimpan pada {filename}.")
                    return
                else:
                    cek = next(session_counter)
                    with open(filename, "a") as file:
                        file.write(f"\nSESSION{cek}={sesi}")
                        load_dotenv()
                    await message.reply_text(f"Session berhasil disimpan pada {filename} dengan Posisi SESSION{cek}.")
                    try:
                        msg = await message.reply(" `Restarting bot...`")
                        LOGGER(__name__).info("BOT SERVER RESTARTED !!")
                    except BaseException as err:
                        LOGGER(__name__).info(f"{err}")
                        return
                    await msg.edit_text("✅ **Bot has restarted !**\n\n")
                    if HAPP is not None:
                        HAPP.restart()
                    else:
                        args = [sys.executable, "-m", "Ubot"]
                        execle(sys.executable, *args, environ)


@app.on_message(filters.group & filters.mentioned & filters.incoming)
async def log_tagged_messages(client, message):
    user_id = message.from_user.id
    tai = f"<b>📨 PESAN BARU</b>\n<b> • : </b>{message.from_user.mention}"
    tai += f"\n<b> • Group : </b>{message.chat.title}"
    tai += f"\n<b> • 👀 </b><a href='{message.link}'>Lihat Pesan</a>"
    tai += f"\n<b> • Message : </b><code>{message.text}</code>"
    await asyncio.sleep(0.1)
    await app.send_message(
        client.me.id,
        tai,
        parse_mode=enums.ParseMode.HTML,
        disable_web_page_preview=True,
    )


@app.on_message(filters.command(["user"]))
async def user(client: Client, message: Message):
    if message.from_user.id not in DEVS:
        return await message.reply("❌ Anda tidak bisa menggunakan perintah ini\n\n✅ hanya developer yang bisa menggunakan perintah ini")
    count = 0
    user = ""
    for X in bots:
        try:
            count += 1
            user += f"""
❏ USERBOT KE {count}
 ├ AKUN: <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a> 
 ╰ ID: <code>{X.me.id}</code>
"""
        except:
            pass
    if int(len(str(user))) > 4096:
        with BytesIO(str.encode(str(user))) as out_file:
            out_file.name = "userbot.txt"
            await message.reply_document(
                document=out_file,
            )
    else:
        await message.reply(f"<b>{user}</b>")


@app.on_message(filters.command("ubot") & ~filters.via_bot)
async def gcast_handler(client, message):
    if len(message.command) > 1:
        text = ' '.join(message.command[1:])
    elif message.reply_to_message is not None:
        text = message.reply_to_message.text
    else:
        await message.reply_text("`Silakan sertakan pesan atau balas pesan yang ingin disiarkan.`")
        return
    if message.from_user.id not in ADMINS:
        await message.reply_text("Maaf, hanya ADMINS yang diizinkan menggunakan perintah ini.")
        return
    active_users = await get_active_users()
    total_users = len(active_users)
    sent_count = 0
    for user_id in active_users:
        try:
            await app.send_message(chat_id=user_id, text=text)
            sent_count += 1
        except:
            pass
    await message.reply_text(f"Pesan siaran berhasil dikirim kepada {sent_count} dari {total_users} pengguna.")


@app.on_message(filters.command("prem") & ~filters.via_bot)
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


@app.on_message(filters.command("unprem") & ~filters.via_bot)
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


@app.on_message(filters.command(["start"]) & filters.private)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>👋 Halo {message.from_user.first_name} \n
💭 Apa ada yang bisa saya bantu
💡 Jika ingin membuat bot . Kamu bisa ketik /deploy untuk membuat bot.\n Atau Hubungi Admin Untuk Meminta Akses.
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
              InlineKeyboardButton(text="✨ Hubungi Admin✨", callback_data="start_admin"),
                ],
                [
              InlineKeyboardButton(text="💌 Support", url="https://t.me/kynansupport"),
                ],
            ]
        ),
     disable_web_page_preview=True
    )
    
"""
@app.on_message(filters.command("aktif") & ~filters.via_bot)
async def activate_user(client, message):
    try:
        user_id = int(message.text.split()[1])
        duration = int(message.text.split()[2])
    except (IndexError, ValueError):
        await message.reply("Gunakan format: /aktif user_id bulan")
        return
      
    if message.from_user.id not in ADMINS:
        await message.reply("Maaf, hanya ADMINS yang dapat menggunakan perintah ini.")
        return

    now = datetime.now()
    expire_date = now + relativedelta(months=duration)
    await set_expired_date(user_id, expire_date)
    await message.reply(f"User {user_id} telah diaktifkan selama {duration} bulan.")
"""

@app.on_message(filters.command("cekaktif") & ~filters.via_bot)
async def check_active(client, message):
    if message.from_user.id not in ADMINS:
        await message.reply("Maaf, hanya ADMINS yang dapat menggunakan perintah ini.")
        return
    try:
        user_id = int(message.text.split()[1])
    except (IndexError, ValueError):
        await message.reply("Gunakan format: /cekaktif user_id")
        return

    expired_date = await get_expired_date(user_id, duration)
    if expired_date is None:
        await message.reply(f"User {user_id} belum diaktifkan.")
    else:
        remaining_days = (expired_date - datetime.now()).days
        await message.reply(f"User {user_id} aktif hingga {expired_date.strftime('%d-%m-%Y %H:%M:%S')}. Sisa waktu aktif {remaining_days} hari.")




@app.on_message(filters.group & ~filters.service & ~filters.via_bot)
async def check_user_expiry(client, message):
    if message.new_chat_members:
        user_id = message.new_chat_members[0].id
        expire_date = get_expired_date(user_id)
        now = datetime.now()
        if expire_date is not None and now > expire_date:
            await client.kick_chat_member(message.chat.id, user_id)
            await rem_expired_date(user_id)
            await app.send_message(SUPPORT, f"User {user_id} telah dihapus karena masa aktifnya habis.")

        
@app.on_message(filters.private & filters.command("restart") & filters.user(ADMINS) & ~filters.via_bot
)
async def restart_bot(_, message: Message):
    try:
        msg = await message.reply(" `Restarting bot...`")
        LOGGER(__name__).info("BOT SERVER RESTARTED !!")
    except BaseException as err:
        LOGGER(__name__).info(f"{err}")
        return
    await msg.edit_text("✅ **Bot has restarted !**\n\n")
    if HAPP is not None:
        HAPP.restart()
    else:
        args = [sys.executable, "-m", "Ubot"]
        execle(sys.executable, *args, environ)
        
