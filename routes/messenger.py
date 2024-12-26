from typing import Optional
from datetime import datetime
from bson import ObjectId
from fastapi import APIRouter, HTTPException

from database.models import Message, MessageCreateRequest
from database.configurations import db


router = APIRouter()

messages_collection = db["Messages"]


def create_message_data(message):
    return {
        "content": message.content,
        "from_user_id": message.from_user_id,
        "to_user_id": message.to_user_id,
        "publish_timestamp": datetime.now(),
        "id": str(ObjectId())
    }


@router.post("/api/messages/")
async def create_message(message: MessageCreateRequest):
    message_data = create_message_data(message)
    await messages_collection.insert_one(message_data)

    return {"id": message_data["id"]}


@router.get("/api/messages/", response_model=Message | list[Message])
async def get_messages(id: Optional[str] = None, from_user_id: Optional[int] = None, to_user_id: Optional[int] = None):
    if id:
        try:
            message = await messages_collection.find_one({"_id": ObjectId(id)})
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid ID format")

        if not message:
            raise HTTPException(status_code=404, detail="Message not found")

        message["_id"] = str(message["_id"])

        return message

    if from_user_id and to_user_id:
        messages = messages_collection.find(
            {
                "$or": [
                    {"from_user_id": from_user_id, "to_user_id": to_user_id},
                    {"from_user_id": to_user_id, "to_user_id": from_user_id}
                ]
            }
        ).sort("publish_timestamp", -1)

        message_list = []
        async for message in messages:
            message["_id"] = str(message["_id"])
            message_list.append(Message(**message))

        return message_list

    else:
        raise HTTPException(status_code=400, detail="Invalid parameters")


@router.put("/api/messages/{id}")
async def update_message(id: str, message: MessageCreateRequest):
    update_data = message.dict()
    update_data["edit_timestamp"] = datetime.now()
    result = await messages_collection.update_one({"id": id}, {"$set": update_data})

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"id": id}


@router.delete("/api/messages/{id}")
async def delete_message(id: str):
    result = await messages_collection.delete_one({"id": id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"id": id}
