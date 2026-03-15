from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
import asyncio


app = FastAPI()

subscribers = []

async def producer():
    i = 0
    while True:
        await asyncio.sleep(2)
        message = {"data": f"message {i}"}
        tasks = []
        for queue in subscribers:
            # await queue.put(message)
            tasks.append(queue.put(message))
        
        await asyncio.gather(*tasks)
        
        i+=1

@app.on_event("startup")
async def start_producer():
    asyncio.create_task(producer())

async def event_generator(request: Request):
    queue = asyncio.Queue()
    subscribers.append(queue)

    try:
        while True:
            if await request.is_disconnected():
                break
            
            event = await queue.get()
            yield event
    finally:
        subscribers.remove(queue)

@app.get("/stream")
async def stream(request: Request):
    return EventSourceResponse(event_generator(request))


        