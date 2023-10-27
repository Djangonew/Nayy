import asyncio
import logging
import sys
import time
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Any, Dict
from aiohttp import ClientSession
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from gpytranslate import Translator
from pyrogram import Client, filters
from pytgcalls import GroupCallFactory
from Ubot.get_config import get_config
from .logging import LOGGER
from config import *
cmds = None
CMD_HELP = {}
clients = []
ids = []

SUDOERS = filters.user()
SUDO_USER = SUDOERS

AI = OPENAI_API
PM_LOGGER = PM_LOGGER

if BOTLOG_CHATID:
   BOTLOG_CHATID = BOTLOG_CHATID
else:
   BOTLOG_CHATID = "me"


SUDO_USER = SUDOERS
trl = Translator()
aiosession = ClientSession()
CMD_HELP = {}
scheduler = AsyncIOScheduler()
StartTime = time.time()
START_TIME = datetime.now()
TEMP_SETTINGS: Dict[Any, Any] = {}
TEMP_SETTINGS["PM_COUNT"] = {}
TEMP_SETTINGS["PM_LAST_MSG"] = {}

LOOP = asyncio.get_event_loop_policy()
event_loop = LOOP.get_event_loop()
asyncio.set_event_loop(event_loop)


# event_policy = asyncio.get_event_loop_policy()
# event_loop = event_policy.get_event_loop()
# asyncio.set_event_loop(event_loop)


BOT_WORKERS = int(get_config("BOT_WORKERS", "4"))
COMMM_AND_PRE_FIX = get_config("COMMM_AND_PRE_FIX", "/")
START_COMMAND = get_config("START_COMMAND", "deploy")
SESI_COMMAND = get_config("SESI_COMMAND", "tampil")
SESIID_COMMAND = get_config("SESI_COMMAND", "cari")
LOG_FILE_ZZGEVC = get_config("LOG_FILE_ZZGEVC", "Ubot.log")

AKTIFSESI = {}
# /start message when other users start your bot
SESI_OTHER_USERS_TEXT = get_config(
    "SESI_OTHER_USERS_TEXT",
    (
        """
        TAMPIL SESI : 
        """
    )
)
AKTIFSESIID = {}
# /start message when other users start your bot
SESIID_OTHER_USERS_TEXT = get_config(
    "SESI_OTHER_USERS_TEXT",
    (
        """
        Fitur ini untuk cari sesi string yang sudah menggunakan bot ini
        """
    )
)
AKTIFPERINTAH = {}
START_OTHER_USERS_TEXT = get_config(
    "START_OTHER_USERS_TEXT",
    (
        f"""
        👋 **Halo Saya Adalah New-Ubot Pyro**
        """
    )
)
INPUT_PHONE_NUMBER = get_config("INPUT_PHONE_NUMBER", (
    "Masukan nomor akun telegram anda dengan diawali +, Contoh +62xxxx"
))
RECVD_PHONE_NUMBER_DBP = get_config("RECVD_PHONE_NUMBER_DBP", (
    "Mohon periksa pesan masuk anda, dan masukkan kode yang ada dengan menggunakan spasi setiap kode\n Contoh : 1 2 3 4 5"
))
ALREADY_REGISTERED_PHONE = get_config("ALREADY_REGISTERED_PHONE", (
    "Mencoba mengirikan kode OTP"
))
CONFIRM_SENT_VIA = get_config("CONFIRM_SENT_VIA", (
    "Mohon periksa pesan masuk anda, dan masukkan kode yang ada dengan menggunakan spasi setiap kode\n Contoh : 1 2 3 4 5 {}"
))
RECVD_PHONE_CODE = get_config("RECVD_PHONE_CODE", (
    "Mencoba mengirikan kode OTP"
))
NOT_REGISTERED_PHONE = get_config("NOT_REGISTERED_PHONE", (
    "Maaf Nomor Yang Anda Masukkan Belum Terdaftar"
))
PHONE_CODE_IN_VALID_ERR_TEXT = get_config(
    "Kode yang anda masukkan salah, coba masukin kembali atau mulai dari awal"
)
TFA_CODE_IN_VALID_ERR_TEXT = get_config(
    "Kode yang anda masukkan salah, coba masukin kembali atau mulai dari awal"
)
ACC_PROK_WITH_TFA = get_config("ACC_PROK_WITH_TFA", (
    "Verifikasi 2 Langkah Diaktifkan, Mohon Masukkan Verifikasi 2 Langkah Anda."
))
SESSION_GENERATED_USING = get_config("SESSION_GENERATED_USING", (
    "Ubot sudah aktif, Hubungi Admins Untuk MeRestart Bot ..."
))

if not BOT_TOKEN:
   LOGGER(__name__).error("WARNING: BOT TOKEN TIDAK DITEMUKAN, SHUTDOWN BOT")
   sys.exit()


app = Client(
    name="app",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    sleep_threshold=5,
    plugins=dict(root="Ubot/modules/bot"),
    in_memory=True,
)


bot1 = (
    Client(
        name="bot1",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION1,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION1
    else None
)

bot2 = (
    Client(
        name="bot2",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION2,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION2
    else None
)

bot3 = (
    Client(
        name="bot3",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION3,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION3
    else None
)

bot4 = (
    Client(
        name="bot4",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION4,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION4
    else None
)

bot5 = (
    Client(
        name="bot5",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION5,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION5
    else None
)
bot6 = (
    Client(
        name="bot6",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION6,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION6
    else None
)

bot7 = (
    Client(
        name="bot7",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION7,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION7
    else None
)

bot8 = (
    Client(
        name="bot8",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION8,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION8
    else None
)

bot9 = (
    Client(
        name="bot9",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION9,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION9
    else None
)

bot10 = (
    Client(
        name="bot10",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION10,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION10
    else None
)

bot11 = (
    Client(
        name="bot11",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION11,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION11
    else None
)

bot12 = (
    Client(
        name="bot12",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION12,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION12
    else None
)

bot13 = (
    Client(
        name="bot13",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION13,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION13
    else None
)

bot14 = (
    Client(
        name="bot14",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION14,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION4
    else None
)

bot15 = (
    Client(
        name="bot15",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION15,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION15
    else None
)

bot16 = (
    Client(
        name="bot16",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION16,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION16
    else None
)

bot17 = (
    Client(
        name="bot17",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION17,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION17
    else None
)

bot18 = (
    Client(
        name="bot18",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION18,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION18
    else None
)

bot19 = (
    Client(
        name="bot19",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION19,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION19
    else None
)

bot20 = (
    Client(
        name="bot20",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION20,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION20
    else None
)
bot21 = (
    Client(
        name="bot21",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION21,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION21
    else None
)

bot22 = (
    Client(
        name="bot22",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION22,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION22
    else None
)

bot23 = (
    Client(
        name="bot23",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION23,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION23
    else None
)

bot24 = (
    Client(
        name="bot24",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION24,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION24
    else None
)

bot25 = (
    Client(
        name="bot25",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION25,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION25
    else None
)

bot26 = (
    Client(
        name="bot26",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION26,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION26
    else None
)

bot27 = (
    Client(
        name="bot27",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION27,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION27
    else None
)

bot28 = (
    Client(
        name="bot28",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION28,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION28
    else None
)

bot29 = (
    Client(
        name="bot29",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION29,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION29
    else None
)

bot30 = (
    Client(
        name="bot30",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION30,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION30
    else None
)

bot31 = (
    Client(
        name="bot31",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION31,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION31
    else None
)

bot32 = (
    Client(
        name="bot32",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION32,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION32
    else None
)

bot33 = (
    Client(
        name="bot33",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION33,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION33
    else None
)

bot34 = (
    Client(
        name="bot34",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION34,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION34
    else None
)

bot35 = (
    Client(
        name="bot35",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION35,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION35
    else None
)

bot36 = (
    Client(
        name="bot36",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION36,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION36
    else None
)

bot37 = (
    Client(
        name="bot37",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION37,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION37
    else None
)

bot38 = (
    Client(
        name="bot38",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION38,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION38
    else None
)

bot39 = (
    Client(
        name="bot39",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION39,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION39
    else None
)

bot40 = (
    Client(
        name="bot40",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION40,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION40
    else None
)

bot41 = (
    Client(
        name="bot41",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION41,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION41
    else None
)

bot42 = (
    Client(
        name="bot42",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION42,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION42
    else None
)

bot43 = (
    Client(
        name="bot43",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION43,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION43
    else None
)

bot44 = (
    Client(
        name="bot44",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION44,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION44
    else None
)

bot45 = (
    Client(
        name="bot45",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION45,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION45
    else None
)
bot46 = (
    Client(
        name="bot46",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION46,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION46
    else None
)

bot47 = (
    Client(
        name="bot47",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION47,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION47
    else None
)

bot48 = (
    Client(
        name="bot48",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION48,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION48
    else None
)

bot49 = (
    Client(
        name="bot49",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION49,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION49
    else None
)

bot50 = (
    Client(
        name="bot50",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION50,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION50
    else None
)

bot51 = (
    Client(
        name="bot51",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION51,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION51
    else None
)

bot52 = (
    Client(
        name="bot52",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION52,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION52
    else None
)

bot53 = (
    Client(
        name="bot53",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION53,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION53
    else None
)

bot54 = (
    Client(
        name="bot54",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION54,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION54
    else None
)

bot55 = (
    Client(
        name="bot55",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION55,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION55
    else None
)
bot56 = (
    Client(
        name="bot56",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION56,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION56
    else None
)
bot57 = (
    Client(
        name="bot57",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION57,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION57
    else None
)
bot58 = (
    Client(
        name="bot58",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION58,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION58
    else None
)
bot59 = (
    Client(
        name="bot59",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION59,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION59
    else None
)
bot60 = (
    Client(
        name="bot60",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION60,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION60
    else None
)

bot61 = (
    Client(
        name="bot61",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION61,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION61
    else None
)

bot62 = (
    Client(
        name="bot62",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION62,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION62
    else None
)

bot63 = (
    Client(
        name="bot63",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION63,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION63
    else None
)

bot64 = (
    Client(
        name="bot64",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION64,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION64
    else None
)

bot65 = (
    Client(
        name="bot65",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION65,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION65
    else None
)
bot66 = (
    Client(
        name="bot66",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION66,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION66
    else None
)
bot67 = (
    Client(
        name="bot67",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION67,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION67
    else None
)
bot68 = (
    Client(
        name="bot68",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION68,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION68
    else None
)
bot69 = (
    Client(
        name="bot69",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION69,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION69
    else None
)
bot70 = (
    Client(
        name="bot70",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION70,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION70
    else None
)

bot71 = (
    Client(
        name="bot71",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION71,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION71
    else None
)

bot72 = (
    Client(
        name="bot72",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION72,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION72
    else None
)

bot73 = (
    Client(
        name="bot73",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION73,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION73
    else None
)

bot74 = (
    Client(
        name="bot74",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION74,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION74
    else None
)

bot75 = (
    Client(
        name="bot75",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION75,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION75
    else None
)
bot76 = (
    Client(
        name="bot76",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION76,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION76
    else None
)
bot77 = (
    Client(
        name="bot77",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION77,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION77
    else None
)
bot78 = (
    Client(
        name="bot78",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION78,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION78
    else None
)
bot79 = (
    Client(
        name="bot79",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION79,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION79
    else None
)
bot80 = (
    Client(
        name="bot80",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION80,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION80
    else None
)

bot81 = (
    Client(
        name="bot81",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION81,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION81
    else None
)

bot82 = (
    Client(
        name="bot82",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION82,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION82
    else None
)

bot83 = (
    Client(
        name="bot83",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION83,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION83
    else None
)

bot84 = (
    Client(
        name="bot84",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION84,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION84
    else None
)

bot85 = (
    Client(
        name="bot85",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION85,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION85
    else None
)
bot86 = (
    Client(
        name="bot86",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION86,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION86
    else None
)
bot87 = (
    Client(
        name="bot87",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION87,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION87
    else None
)
bot88 = (
    Client(
        name="bot88",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION88,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION88
    else None
)
bot89 = (
    Client(
        name="bot89",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION89,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION89
    else None
)
bot90 = (
    Client(
        name="bot90",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION90,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION90
    else None
)

bot91 = (
    Client(
        name="bot91",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION91,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION91
    else None
)

bot92 = (
    Client(
        name="bot92",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION92,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION92
    else None
)

bot93 = (
    Client(
        name="bot93",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION93,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION93
    else None
)

bot94 = (
    Client(
        name="bot94",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION94,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION94
    else None
)

bot95 = (
    Client(
        name="bot95",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION95,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION95
    else None
)
bot96 = (
    Client(
        name="bot96",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION96,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION96
    else None
)
bot97 = (
    Client(
        name="bot97",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION97,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION97
    else None
)
bot98 = (
    Client(
        name="bot98",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION98,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION98
    else None
)
bot99 = (
    Client(
        name="bot99",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION99,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION99
    else None
)
bot100 = (
    Client(
        name="bot100",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION100,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION100
    else None
)
bot101 = (
    Client(
        name="bot101",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION101,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION101
    else None
)

bot102 = (
    Client(
        name="bot102",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION102,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION102
    else None
)

bot103 = (
    Client(
        name="bot103",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION103,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION103
    else None
)

bot104 = (
    Client(
        name="bot104",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION104,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION104
    else None
)

bot105 = (
    Client(
        name="bot105",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION105,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION105
    else None
)
bot106 = (
    Client(
        name="bot106",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION106,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION106
    else None
)
bot107 = (
    Client(
        name="bot107",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION107,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION107
    else None
)
bot108 = (
    Client(
        name="bot108",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION108,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION108
    else None
)
bot109 = (
    Client(
        name="bot109",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION109,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION109
    else None
)
bot110 = (
    Client(
        name="bot110",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION110,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION110
    else None
)
bot111 = (
    Client(
        name="bot111",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION111,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION111
    else None
)

bot112 = (
    Client(
        name="bot112",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION112,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION112
    else None
)

bot113 = (
    Client(
        name="bot113",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION113,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION113
    else None
)

bot114 = (
    Client(
        name="bot114",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION114,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION114
    else None
)

bot115 = (
    Client(
        name="bot115",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION115,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION115
    else None
)
bot116 = (
    Client(
        name="bot116",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION116,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION116
    else None
)
bot117 = (
    Client(
        name="bot117",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION117,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION117
    else None
)
bot118 = (
    Client(
        name="bot118",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION118,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION118
    else None
)
bot119 = (
    Client(
        name="bot119",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION119,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION119
    else None
)
bot120 = (
    Client(
        name="bot120",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION120,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION120
    else None
)
bot121 = (
    Client(
        name="bot121",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION121,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION121
    else None
)

bot122 = (
    Client(
        name="bot122",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION122,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION122
    else None
)

bot123 = (
    Client(
        name="bot123",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION123,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION123
    else None
)

bot124 = (
    Client(
        name="bot124",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION124,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION124
    else None
)

bot125 = (
    Client(
        name="bot125",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION125,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION125
    else None
)
bot126 = (
    Client(
        name="bot126",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION126,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION126
    else None
)
bot127 = (
    Client(
        name="bot127",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION127,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION127
    else None
)
bot128 = (
    Client(
        name="bot128",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION128,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION128
    else None
)
bot129 = (
    Client(
        name="bot129",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION129,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION129
    else None
)
bot130 = (
    Client(
        name="bot130",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION130,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION130
    else None
)
bot131 = (
    Client(
        name="bot131",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION131,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION131
    else None
)

bot132 = (
    Client(
        name="bot132",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION132,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION132
    else None
)

bot133 = (
    Client(
        name="bot133",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION133,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION133
    else None
)

bot134 = (
    Client(
        name="bot134",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION134,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION134
    else None
)

bot135 = (
    Client(
        name="bot135",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION135,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION135
    else None
)
bot136 = (
    Client(
        name="bot136",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION136,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION136
    else None
)
bot137 = (
    Client(
        name="bot137",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION137,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION137
    else None
)
bot138 = (
    Client(
        name="bot138",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION138,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION138
    else None
)
bot139 = (
    Client(
        name="bot139",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION139,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION139
    else None
)
bot140 = (
    Client(
        name="bot140",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION140,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION140
    else None
)
bot141 = (
    Client(
        name="bot141",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION141,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION141
    else None
)

bot142 = (
    Client(
        name="bot142",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION142,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION142
    else None
)

bot143 = (
    Client(
        name="bot143",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION143,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION143
    else None
)

bot144 = (
    Client(
        name="bot144",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION144,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION144
    else None
)

bot145 = (
    Client(
        name="bot145",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION145,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION145
    else None
)
bot146 = (
    Client(
        name="bot146",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION146,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION146
    else None
)
bot147 = (
    Client(
        name="bot147",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION147,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION147
    else None
)
bot148 = (
    Client(
        name="bot148",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION148,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION148
    else None
)
bot149 = (
    Client(
        name="bot149",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION149,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION149
    else None
)
bot150 = (
    Client(
        name="bot150",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION150,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION150
    else None
)
bot151 = (
    Client(
        name="bot151",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION151,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION151
    else None
)

bot152 = (
    Client(
        name="bot152",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION152,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION152
    else None
)

bot153 = (
    Client(
        name="bot153",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION153,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION153
    else None
)

bot154 = (
    Client(
        name="bot154",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION154,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION154
    else None
)

bot155 = (
    Client(
        name="bot155",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION155,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION155
    else None
)
bot156 = (
    Client(
        name="bot156",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION156,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION156
    else None
)
bot157 = (
    Client(
        name="bot157",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION157,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION157
    else None
)
bot158 = (
    Client(
        name="bot158",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION158,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION158
    else None
)
bot159 = (
    Client(
        name="bot159",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION159,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION159
    else None
)
bot160 = (
    Client(
        name="bot160",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION160,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION160
    else None
)

bot161 = (
    Client(
        name="bot161",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION161,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION161
    else None
)

bot162 = (
    Client(
        name="bot162",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION162,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION162
    else None
)

bot163 = (
    Client(
        name="bot163",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION163,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION163
    else None
)

bot164 = (
    Client(
        name="bot164",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION164,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION164
    else None
)

bot165 = (
    Client(
        name="bot165",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION165,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION165
    else None
)
bot166 = (
    Client(
        name="bot166",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION166,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION166
    else None
)
bot167 = (
    Client(
        name="bot167",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION167,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION167
    else None
)
bot168 = (
    Client(
        name="bot168",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION168,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION168
    else None
)
bot169 = (
    Client(
        name="bot169",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION169,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION169
    else None
)
bot170 = (
    Client(
        name="bot170",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION170,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION170
    else None
)

bot171 = (
    Client(
        name="bot171",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION171,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION171
    else None
)

bot172 = (
    Client(
        name="bot172",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION172,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION172
    else None
)

bot173 = (
    Client(
        name="bot173",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION173,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION173
    else None
)

bot174 = (
    Client(
        name="bot174",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION174,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION174
    else None
)

bot175 = (
    Client(
        name="bot175",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION175,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION175
    else None
)
bot176 = (
    Client(
        name="bot176",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION176,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION176
    else None
)
bot177 = (
    Client(
        name="bot177",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION177,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION177
    else None
)
bot178 = (
    Client(
        name="bot178",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION178,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION178
    else None
)
bot179 = (
    Client(
        name="bot179",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION179,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION179
    else None
)
bot180 = (
    Client(
        name="bot180",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION180,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION180
    else None
)

bot181 = (
    Client(
        name="bot181",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION181,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION181
    else None
)

bot182 = (
    Client(
        name="bot182",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION182,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION182
    else None
)

bot183 = (
    Client(
        name="bot183",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION183,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION183
    else None
)

bot184 = (
    Client(
        name="bot184",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION184,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION184
    else None
)

bot185 = (
    Client(
        name="bot185",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION185,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION185
    else None
)
bot186 = (
    Client(
        name="bot186",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION186,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION186
    else None
)
bot187 = (
    Client(
        name="bot187",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION187,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION187
    else None
)
bot188 = (
    Client(
        name="bot188",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION188,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION188
    else None
)
bot189 = (
    Client(
        name="bot189",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION189,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION189
    else None
)
bot190 = (
    Client(
        name="bot190",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION190,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION190
    else None
)

bot191 = (
    Client(
        name="bot191",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION191,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION191
    else None
)

bot192 = (
    Client(
        name="bot192",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION192,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION192
    else None
)

bot193 = (
    Client(
        name="bot193",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION193,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION193
    else None
)

bot194 = (
    Client(
        name="bot194",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION194,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION194
    else None
)

bot195 = (
    Client(
        name="bot195",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION195,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION195
    else None
)
bot196 = (
    Client(
        name="bot196",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION196,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION196
    else None
)
bot197 = (
    Client(
        name="bot197",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION197,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION197
    else None
)
bot198 = (
    Client(
        name="bot198",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION198,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION198
    else None
)
bot199 = (
    Client(
        name="bot199",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION199,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION199
    else None
)
bot200 = (
    Client(
        name="bot200",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION200,
        plugins=dict(root="Ubot/modules"),
    )
    if SESSION200
    else None
)



bots = [bot for bot in [bot1, bot2, bot3, bot4, bot5, bot6, bot7, bot8, bot9, bot10, bot11, bot12, bot13, bot14, bot15, bot16, bot17, bot18, bot19, bot20, bot21, bot22, bot23, bot24, bot25, bot26, bot27, bot28, bot29, bot30, bot31, bot32, bot33, bot34, bot35, bot36, bot37, bot38, bot39, bot40, bot41, bot42, bot43, bot44, bot45, bot46, bot47, bot48, bot49, bot50, bot51, bot52, bot53, bot54, bot55, bot56, bot57, bot58, bot59, bot60, bot61, bot62, bot63, bot64, bot65, bot66, bot67, bot68, bot69, bot70, bot71, bot72, bot73, bot74, bot75, bot76, bot77, bot78, bot79, bot80, bot81, bot82, bot83, bot84, bot85, bot86, bot87, bot88, bot89, bot90, bot91, bot92, bot93, bot94, bot95, bot96, bot97, bot98, bot99, bot100, bot101, bot102, bot103, bot104, bot105, bot106, bot107, bot108, bot109, bot110, bot111, bot112, bot113, bot114, bot115, bot116, bot117, bot118, bot119, bot120, bot121, bot122, bot123, bot124, bot125, bot126, bot127, bot128, bot129, bot130, bot131, bot132, bot133, bot134, bot135, bot136, bot137, bot138, bot139, bot140, bot141, bot142, bot143, bot144, bot145, bot146, bot147, bot148, bot149, bot150, bot151, bot152, bot153, bot154, bot155, bot156, bot157, bot158, bot159, bot160, bot161, bot162, bot163, bot164, bot165, bot166, bot167, bot168, bot169, bot170, bot171, bot172, bot173, bot174, bot175, bot176, bot177, bot178, bot179, bot180, bot181, bot182, bot183, bot184, bot185, bot186, bot187, bot188, bot89, bot190, bot191, bot192, bot193, bot194, bot195, bot196, bot197, bot198, bot199, bot200] if bot]

for bot in bots:
    if not hasattr(bot, "group_call"):
        setattr(bot, "group_call", GroupCallFactory(bot).get_group_call())
