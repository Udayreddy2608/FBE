from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()


    

# @app.get("/stream")
# async def stream():
#     return StreamingResponse(event_generator(), media_type= 'text/event-stream')

import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.connections = {}

    def add(self, user_id, queue):
        self.connections[user_id] = queue

    def remove(self, user_id):
        self.connections.pop(user_id, None)

    async def send(self, user_id, message):
        if user_id in self.connections:
            await self.connections[user_id].put(message)

manager = ConnectionManager()


@app.get("/stream")
async def stream(request: Request):
    user_id = request.query_params.get("user_id")

    if not user_id:
        return {"error": "user_id required"}

    queue = asyncio.Queue()
    manager.add(user_id, queue)

    async def event_generator():
        try:
            for i in range(1,101):
                if await request.is_disconnected():
                    break
                send_message = {"data": f"message: {i}"}
                await manager.send(user_id= user_id, message= send_message)
                message = await queue.get()
                yield f"{message}\n\n"
                await asyncio.sleep(1)

        finally:
            manager.remove(user_id)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


