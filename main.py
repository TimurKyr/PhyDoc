from fastapi import FastAPI

from routes import messenger, websocket


app = FastAPI()

app.include_router(messenger.router)
app.include_router(websocket.router)


@app.get("/")
async def root():
    return {"message": "My Messenger API"}
