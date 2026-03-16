from fastapi import FastAPI
import asyncio
import time

app = FastAPI()

data_ready = False

@app.get("/data")
async def get_data():
    if data_ready:
        return {"data": "Here is your data"}
    else:
        return {"status": "not ready"}
        

@app.get("/long-poll")
async def long_poll():
    i = 0
    while not data_ready:
        if i == 10:
            return {"data": "here is your data"}
        print(f"Iteration: {i}")
        await asyncio.sleep(2)
        i += 1
    

