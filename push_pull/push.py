from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
import asyncio


app = FastAPI()


# ------------------------------------ DESIGN PATTERN 1 ------------------------------------

"""
dedicated generator for each client

Client A → generator A
Client B → generator B
Client C → generator C

each generator produces its own message

"""

async def event_generator():
    i = 0
    while True:
        await asyncio.sleep(2)
        yield {"data": f"message {i}"}
        i += 1


@app.get("/stream/dp1")
async def stream():
    return EventSourceResponse(event_generator())


#------------------------------------ DESIGN PATTERN 2 ------------------------------------

"""
Single producer collects all the messages, clients consume messages from the producer

Producer
   ↓
async queue
   ↓
many clients consume

"""

subscribers = []

async def producer():
    i = 0

    while True:
        await asyncio.sleep(2)
        message = {"data": f"message {i}"}

        for queue in subscribers:
            await queue.put(message) # Here put happens sequentially...it become bottleneck if the number of subscriber increased.
        
        i += 1

@app.on_event("startup")
async def start_producer():
    asyncio.create_task(producer()) # The producer starts when the app is started
                                    # so the events will be put into the queue
                                    # So each client will have a queue and the client consumes the event from the queue


"""
For example:

Producer started when app started:

A client is connected: subscribers become -> [Queue1]

Lets say by the time the 1st client is connected producer emitted 2 events -> msg1 and msg2 

-> these 2 events are pushed to queue1 and they are consumed by the client

When client 2 is connected: subscribers becomes -> [Queue1, Queue2]

-> by the time client2 joined lets say generator emitted 9 events and the 10th is emitted after the client 2 joined

so all the events emitted by producer after client 2 joined will be added to the Queue2 and put to Queue2]

Queue2 becomes -> [event10, event11]
"""


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

@app.get("/stream/dp2")
async def stream(request: Request):
    return EventSourceResponse(event_generator(request))


