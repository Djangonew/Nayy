from pyrogram.filters import chat
from pyrogram import filters, Client
from . import db
from typing import Dict, List, Union

collection = db["pmpermit"]

PMPERMIT_MESSAGE = (
    "**Jangan spam atau Anda akan diblokir, jadi berhati-hatilah untuk mengirim pesan pesan!**"
)

BLOCKED = "**Spammer, blocked!**"

LIMIT = 5

USERS_AND_WARNS = {}

FLOOD_CTRL = 0

ALLOWED = []


async def set_pm(user_id, value: bool):
    collection.update_one(
        {"user_id": user_id},
        {"$set": {"pmpermit": value}},
        upsert=True
    )


async def set_pm_message(user_id: int, text: str):
    doc = {"user_id": user_id, "pmpermit_message": text}
    await collection.update_one(
        {"user_id": user_id},
        {"$set": doc},
        upsert=True)

async def set_limit(user_id: int, limit):
    doc = {"user_id": user_id, "limit": limit}
    await collection.update_one(
      {"user_id": user_id},
      {"$set": doc},
      upsert=True)

async def set_block_message(user_id: int, text: str):
    doc = {"user_id": user_id, "block_message": text}
    await collection.update_one(
      {"user_id": user_id},
      {"$set": doc},
      upsert=True)
        
async def get_pm_settings(user_id: int):
    result = await collection.find_one({"user_id": user_id})
    if not result:
        return False
    pmpermit = result["pmpermit"]
    pm_message = result.get("pmpermit_message", PMPERMIT_MESSAGE)
    block_message = result.get("block_message", BLOCKED)
    limit = result.get("limit", LIMIT)
    return pmpermit, pm_message, limit, block_message


async def allow_user(chat_id: int, user_id: int):
    doc = {"chat_id": chat_id, "user_id": user_id, "Approved": True}
    r = await collection.find_one({"chat_id": chat_id, "user_id": user_id})
    if r:
      await collection.update_one(
        {"user_id": user_id, "chat_id": chat_id},
        {"$set": {"Approved": True}})
    else:
        await collection.insert_one(doc)


async def deny_user(chat_id: int, user_id: int):
    await collection.update_one(
      {"chat_id": chat_id, "user_id": user_id},
      {"$set": {"Approved": False}})

async def is_allowed(chat_id):
    r = await collection.find_one({"user_id": chat_id})
    return r and r["Approved"] == True


async def get_approved_users():
    results = await collection.find_one({"user_id": "Approved"})
    if results:
        return results["users"]
    else:
        return []
    
async def pm_guard(chat_id: int, user_id: int):
    result = await collection.find_one(
      {"chat_id": chat_id, "user_id": user_id})
    if not result:
       return False
    if not result["pmpermit"]:
       return False
    else:
       return True