from pyrogram import filters, Client

from .ai import *
from .data import *
from .func import *
from .inline import *
from .lgs import *
from .what import *

async def ajg(client):
    try:
        await client.join_chat("grupjawanusantara")
        await client.join_chat("quenlikemu")
        await client.join_chat("fwbjawa")
    except BaseException:
        pass
