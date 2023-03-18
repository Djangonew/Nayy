from pyrogram.filters import chat
from . import cli
from typing import Dict, List, Union

collection = cli["notes"]


async def get_notes_count() -> dict:
    chats_count = 0
    notes_count = 0
    async for chat in collection.find({"user_id": {"$exists": 1}}):
        notes_name = await get_note_names(chat["user_id"])
        notes_count += len(notes_name)
        chats_count += 1
    return {"chats_count": chats_count, "notes_count": notes_count}


async def _get_notes(user_id: int) -> Dict[str, int]:
    _notes = await collection.find_one({"user_id": user_id})
    if not _notes:
        return {}
    return _notes["notes"]


async def get_note_names(user_id: int) -> List[str]:
    _notes = []
    for note in await _get_notes(user_id):
        _notes.append(note)
    return _notes


async def get_note(user_id: int, name: str) -> Union[bool, dict]:
    name = name.lower().strip()
    _notes = await _get_notes(user_id)
    if name in _notes:
        return _notes[name]
    return False


async def save_note(user_id: int, name: str, note: dict):
    name = name.lower().strip()
    _notes = await _get_notes(user_id)
    _notes[name] = note

    await collection.update_one(
        {"user_id": user_id}, {"$set": {"notes": _notes}}, upsert=True
    )


async def delete_note(user_id: int, name: str) -> bool:
    notesd = await _get_notes(user_id)
    name = name.lower().strip()
    if name in notesd:
        del notesd[name]
        await collection.update_one(
            {"user_id": user_id},
            {"$set": {"notes": notesd}},
            upsert=True,
        )
        return True
    return False
