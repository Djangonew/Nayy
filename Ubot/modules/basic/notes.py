from asyncio import sleep
from pyrogram import Client, filters
from ubotlibs.ubot.database.notesdb import *
from pyrogram.types import Message
from ubotlibs.ubot.utils.tools import *
from . import *
from ubotlibs.ubot.database.accesdb import *




@Ubot(["save", "Save"], "")
async def simpan_note(client, message):
    name = get_arg(message)
    user_id = message.from_user.id
    msg = message.reply_to_message
    if not msg:
        return await message.reply("`Silakan balas ke pesan.`")
    anu = await msg.forward(BOTLOG_CHATID)
    msg_id = anu.id
    await client.send_message(BOTLOG_CHATID,
        f"#NOTE\nKEYWORD: {name}"
        "\n\nPesan berikut disimpan sebagai data balasan catatan untuk obrolan, mohon jangan dihapus !!",
    )
    await sleep(1)
    await save_note(user_id, name, msg_id)
    await message.reply(f"**Berhasil menyimpan catatan dengan nama** `{name}`")


@Ubot(["Get", "get"], "")
async def panggil_notes(client, message):
    name = get_arg(message)
    user_id = message.from_user.id
    _note = await get_note(user_id, name)
    if not _note:
        return await message.reply("`Tidak ada catatan seperti itu.`")
    msg_o = await client.get_messages(BOTLOG_CHATID, _note)
    await msg_o.copy(message.chat.id, reply_to_message_id=message.id)


@Ubot(["rm", "Rm"], "")
async def remove_notes(client, message):
    name = get_arg(message)
    user_id = message.from_user.id
    deleted = await delete_note(user_id, name)
    if deleted:
        await message.reply("**Berhasil Menghapus Catatan:** `{}`".format(name))
    else:
        await message.reply("**Tidak dapat menemukan catatan:** `{}`".format(name))


@Ubot(["notes", "Notes"], "")
async def get_notes(client, message):
    user_id = message.from_user.id
    _notes = await get_note_names(user_id)
    if not _notes:
        return await message.reply("**Tidak ada catatan.**")
    msg = f"**➣ Daftar catatan**\n\n"
    for note in _notes:
        msg += f"**•** `{note}`\n"
    await message.reply(msg)


add_command_help(
    "notes",
    [
        [f" save [text/reply]",
            "Simpan pesan ke Group. (bisa menggunakan stiker)"],
        [f" get [nama]",
            "Ambil catatan ke tersimpan"],
        [f" notes",
            "Lihat Daftar Catatan"],
        [f" rm [nama]",
            "Menghapus nama catatan"],
    ],
)
