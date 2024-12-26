import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from database.configurations import db


router = APIRouter()

messages_collection = db["Messages"]


@router.websocket("/api/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            random_message = await messages_collection.aggregate([
                {"$sample": {"size": 1}}
            ]).to_list(1)

            if random_message:
                message = random_message[0]
                content = message.get("content")
                from_user = message.get("from_user_id")
                to_user = message.get("to_user_id")
                timestamp = message.get("publish_timestamp")

                await websocket.send_text(f"Random message: {content} | From: {from_user} To: {to_user} | Time: {timestamp}")

            await asyncio.sleep(1)

    except WebSocketDisconnect:
        print("Client disconnected")
