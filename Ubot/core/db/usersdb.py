from pyrogram.filters import chat
from . import cli
from typing import Dict, List, Union
from datetime import datetime, timedelta

collection = cli["active_users"]


async def add_user(user_id):
    user = {
        "_id": user_id,
        "last_active": datetime.now()
    }
    collection.replace_one({"_id": user_id}, user, upsert=True)

async def remove_user(user_id):
    collection.delete_one({"_id": user_id})

async def get_active_users():
    return [doc["_id"] async for doc in collection.find()]


async def add_ubot(user_id, api_id, api_hash, session_string):
    ubot = {
        "user_id": user_id,
        "api_id": api_id,
        "api_hash": api_hash,
        "session_string": session_string,
    }
    result = await collection.update_one(
        {"user_id": user_id},
        {"$set": ubot},
        upsert=True
    )
    return result.acknowledged


async def remove_ubot(user_id, session_string):
    result = await collection.delete_one({
        "user_id": user_id,
        "session_string": session_string
    })
    return result.deleted_count > 0


async def get_userbots():
    data = []
    async for ubot in collection.find({"user_id": {"$exists": 1}}):
        data.append(
            dict(
                name=str(ubot["user_id"]),
                api_id=ubot["api_id"],
                api_hash=ubot["api_hash"],
                session_string=ubot["session_string"],
            )
        )
    return data