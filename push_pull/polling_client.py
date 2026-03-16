import requests
import time


url = "http://localhost:8000/data"

# while True:
#     result = requests.get(url).json()
#     print("Server response:", result)

#     if "data" in result:
#         print("Got the data")
#         break

#     time.sleep(2)


# url = "http://localhost:8000/long-poll"
# result = requests.get(url)
# print(result.json())

import asyncio
import httpx


async def poll():
    async with httpx.AsyncClient() as client:
        while True:
            result = await client.get(url)
            data = result.json()
            print(data)

            if "data" in data:
                break

            await asyncio.sleep(2)


asyncio.run(poll())