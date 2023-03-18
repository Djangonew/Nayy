from pyrogram import Client, filters
from pyrogram.types import Message, InputMediaUploadedDocument, InputMediaUploadedPhoto
from pyrogram.types import InputPeerSelf, InputStickerSetID, InputStickerSetItem
from pyrogram.raw.functions.messages import UploadMediaRequest
from . import *

@Client.on_message(filters.command("packkang", cmds) & filters.me)
async def pack_kang(client, message):
    if not message.reply_to_message:
        await message.reply_text("Balas stiker dengan perintah /packkang untuk mengemas stiker ke pack")
        return
    chat_id = message.chat.id
    user_id = message.from_user.id
    packname = message.text.split()[1] if len(message.text.split()) > 1 else None
    animated = False
    if "animated" in message.text:
        animated = True
    elif "gif" in message.reply_to_message.document.mime_type:
        animated = True
    packname = packname.replace(" ", "_") if packname is not None else "sticker"
    packtitle = packname.title()
    packnick = f"@{client.username}'s {packtitle} pack"
    packshort = f"{client.username}_{packname.lower()}"
    response = await message.reply_text("Mengunduh dan mengemas stiker, silakan tunggu sebentar...")
    files = await message.reply_to_message.download()
    inputs = await get_input_documents(client, files)
    # create new sticker pack
    stickerset = await create_sticker_pack(client, user_id, packnick, packshort, animated)
    pack_id = stickerset.pack.id
    # add stickers to pack
    for item in inputs:
        try:
            result = await client.send(
                UploadMediaRequest(
                    media=item,
                    peer=InputPeerSelf(),
                    media_type="sticker",
                    message=f"{packnick}",
                    random_id=client.rnd_id()
                )
            )
            sticker = InputStickerSetItem(
                document=result.updates[1].media.document,
                emoji=result.updates[1].message.media.document.attributes[1].alt
            )
            await client.send(
                AddStickerToSet(
                    stickerset=InputStickerSetID(id=pack_id, access_hash=stickerset.pack.access_hash),
                    sticker=sticker
                )
            )
        except Exception as e:
            await response.edit_text(f"Gagal menambahkan stiker. Error: {e}")
            return
    await response.edit_text(f"Stiker telah berhasil dikemas ke pack {packnick}")

async def get_input_documents(client, files):
    inputs = []
    count = 0
    for file in files:
        count += 1
        if file.endswith((".tgs", ".webm")):
            media = await client.send_message("me", file=file)
            inputs.append(
                InputMediaUploadedDocument(
                    file=media.document,
                    mime_type=media.document.mime_type,
                    attributes=media.document.attributes,
                    thumb=media.document.thumb,
                    caption=media.caption
                )
            )
        else:
            inputs.append(
                InputMediaUploadedPhoto(
                    file=await client.upload_media(file),
                    caption=f"Uploaded {file}"
                )
            )
        if count % 5 == 0:
            await client.progress(0, count, f"Uploaded {count} files.")
    return inputs
