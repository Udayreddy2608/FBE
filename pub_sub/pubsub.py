# PubSub -> it is a communication pattern where producers emit events without knowing who consumes them
# Consumer consume events without knowing which producer emitted them

# This is complete decoupling

"""
1. Space decoupling
producer -> "order created"
         |
        Broker
         |
    Service A, B , C (Unknown to the producer)


2. Time Decoupling
    -> Producer and consumer dont run at the same time
    example:
        -> Producer publishes at 10:00
        -> Consumer processes at 10:05

3. Synchronization decoupling
    -> Producer do NOT wait for the consumer
    -> Fully async


----------------STEP-BY-STEP FLOW----------------

1. Producer -> publish (event)
2. Broker -> receives (event)
3. Broker -> Finds subscribers of topic
4. Broker -> delivers event
5. Consumer -> processes event


what is a topic?
-> Topic is a logical channel
examples:
-> order created
-> payment failed
-> user signed up


Core models inside pub/sub

Model 1: FAN OUT model
    -> Single producer multiple consumers
    -> All consumers receive the same event


Model 2: Consumer groups
    -> Only one consumer processes message
"""


from collections import defaultdict
import asyncio

class PubSub:
    def __init__(self):
        self.topics = defaultdict(asyncio.Queue)
        self.subscribers = defaultdict(list)
    
    async def publish(self, topic, message):
        await self.topics[topic].put(message) # Here we are publishing the message to the queue
    
    def subscribe(self, topic:str, handler, workers = 1): 
        # if topic not in self.topics:
        #     return
        
        # for handler in self.topics[topic]:
        #     asyncio.create_task(handler(message))
        for _ in range(workers):
            async def worker():
                while True:
                    msg = await self.topics[topic].get() # Consumers consume the message from the queue
                    await handler(msg)
            asyncio.create_task(worker())

# async def service_a(msg):
#     print("A got: ", msg)

# async def service_b(msg):
#     print("B got: ", msg)

# async def service_c(msg):
#     print(f"C got: ", msg)

async def consumer(msg):
    print("Processed: ", msg)

async def send_email(msg):
    print(f"email_sent_to: ", msg)

async def main():
    # bus = PubSub()
    # bus.subscribe("order_created", service_a)
    # bus.subscribe("order_created", service_b)
    # bus.subscribe("payment_failed", service_c)
    # await bus.publish("order_created", {"id": 1})
    # await bus.publish("payment_failed", {"payment_id":"qwertyuiop"})
    # await asyncio.sleep(1)
    bus = PubSub()
    # bus.subscribe("payments", consumer)
    bus.subscribe("emails", send_email, workers=3)
    for i in range(1000):
        # await bus.publish("payments",i)
        await bus.publish("emails", i)
    await asyncio.sleep(2)


asyncio.run(main())