from . import db

collection = db["pmpermit"]

PMPERMIT_MESSAGE = (
    "**Jangan spam atau Anda akan diblokir, jadi berhati-hatilah untuk mengirim pesan pesan!**"
)

BLOCKED = "**Blokir !**"

LIMIT = 5


async def set_pm(user_id: int, value: bool):
    doc = {"_id": user_id, "pmpermit": value}
    doc2 = {"_id": "Approved", "users": []}
    r = await collection.find_one({"_id": user_id})
    r2 = await collection.find_one({"_id": "Approved"})
    if r:
        await collection.update_one({"_id": user_id}, {"$set": {"pmpermit": value}})
    else:
        await collection.insert_one(doc)
    if not r2:
        await collection.insert_one(doc2)


async def set_permit_message(user_id: int, text):
    doc = {"_id": user_id, "pmpermit_message": text}
    r = await collection.find_one({"_id": user_id})
    if r:
        await collection.update_one({"_id": user_id}, {"$set": {"pmpermit_message": text}})
    else:
        await collection.insert_one(doc)


async def set_block_message(user_id: int, text):
    doc = {"_id": user_id, "block_message": text}
    r = await collection.find_one({"_id": user_id})
    if r:
        await collection.update_one({"_id": user_id}, {"$set": {"block_message": text}})
    else:
        await collection.insert_one(doc)


async def set_limit(user_id: int, limit):
    doc = {"_id": user_id, "limit": limit}
    r = await collection.find_one({"_id": user_id})
    if r:
        await collection.update_one({"_id": user_id}, {"$set": {"limit": limit}})
    else:
        await collection.insert_one(doc)



async def get_pm_settings():
    result = await collection.find_one({"_id": user_id})
    if not result:
        return False
    pmpermit = result["pmpermit"]
    pm_message = result.get("pmpermit_message", PM_PERMIT_MESSAGE)
    block_message = result.get("block_message", BLOCKED_MESSAGE)
    limit = result.get("limit", LIMIT)
    return pmpermit, pm_message, limit, block_message



async def allow_user(chat):
    doc = {"_id": "Approved", "users": [chat]}
    r = await collection.find_one({"_id": "Approved"})
    if r:
        await collection.update_one({"_id": "Approved"}, {"$push": {"users": chat}})
    else:
        await collection.insert_one(doc)


async def get_approved_users():
    results = await collection.find_one({"_id": "Approved"})
    if results:
        return results["users"]
    else:
        return []


async def deny_user(chat):
    await collection.update_one({"_id": "Approved"}, {"$pull": {"users": chat}})


async def pm_guard():
    result = await collection.find_one({"_id": user_id})
    if not result:
        return False
    if not result["pmpermit"]:
        return False
    else:
        return True

