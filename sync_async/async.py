import asyncio
import time
# coroutine is a function that can pause and resume execution
# It must be executed in the event loop


async def fetch_data(task_id):
    """ 
        for example:
            an event loop has 5 events of fetch_data
            execution steps:
                fetch_data (1) -> says pause me for 2 seconds
                fetch_data (2) -> says pause me for 2 seconds
                fetch_data (3) -> says pause me for 2 seconds
                fetch_data (4) -> says pause me for 2 seconds
                fetch_data (5) -> says pause me for 2 seconds
            
            The event loop doesn't stop at the 1st one...it pauses the 1st coroutine and goes to the second one as so on...

            so instead of waiting 2 seconds at each steps all steps will be waiting for the same 2 seconds at the same time...

            so the resulting time will be 2 seconds not 10 seconds

            Even if the number of coroutines in the event loop is 10...the total time will be 2 seconds
    """
    print(f"start task: {task_id}")
    await asyncio.sleep(2) # this is different from normal time.sleep(), what it does is it says pause me for 2 seconds and go to the next coroutine
    print(f"End task: {task_id}")
    return f"data: {task_id}"

async def main():
    start = asyncio.get_event_loop().time()

    tasks = [fetch_data(i) for i in range(10000)] # fetch_data doesn't run immediately, it returns a coroutine object which the event loop can schedule.
                                                  # returns 10000 coroutine objects [fetch_data(0), fetch_data(1), fetch_data(2).......fetch_data(9999)].

    results = await asyncio.gather(*tasks) # gather schedules all the coroutines in the event loop, 
                                           # waits until all finish and returns the results in the same order.

    print(results)

    print(f"Time taken:", asyncio.get_event_loop().time() - start)

# asyncio.run(main())

"""
t=0

main() starts
create 5 coroutines
gather() schedules them

task0 start
task1 start
task2 start
task3 start
task4 start

all hit await sleep(2)
all pause

event loop idle

t=2

task0 resume
task1 resume
task2 resume
task3 resume
task4 resume

all finish
gather returns results
"""

async def main():
    start = time.time()
    await fetch_data(1)
    await fetch_data(2)
    print(f"Time taken: {time.time() - start}")


# asyncio.run(main())

async def main():
    start = time.time()
    task1 = asyncio.create_task(fetch_data(1))
    task2 = asyncio.create_task(fetch_data(2))

    await task1
    await task2
    print(f"Time taken: {time.time() - start}")


# asyncio.run(main())

"""
differences: 

asyncio.gather()                and             asyncio.create_task()
-> used when you want all                       -> Used when you want background execution
the results together        
-> runs concurrently
-> waits for all tasks to 
complete
"""

async def main():
    asyncio.create_task(fetch_data(1))



async def main():
    asyncio.create_task(fetch_data(1))
    await asyncio.sleep(2)

# asyncio.run(main())

import requests

def http_counter():
    urls = [
    "https://httpbin.org/delay/4",
    "https://httpbin.org/delay/4",
    "https://httpbin.org/delay/4"
    ]
    start = time.time()
    for url in urls:
        response = requests.get(url)
        print(response.status_code)
    print(f"Time taken: {time.time() - start}")

http_counter()

import aiohttp

urls = [
    "https://httpbin.org/delay/4",
    "https://httpbin.org/delay/4",
    "https://httpbin.org/delay/4"
]

async def fetch(session,url):
    async with session.get(url) as response:
        return response.status

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session,url) for url in urls]
        results = await asyncio.gather(*tasks)
        print(results)

start = time.time()
asyncio.run(main())
print(f"Time Taken: {time.time() - start}")