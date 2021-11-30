import time
import asyncio
import random
import requests
import math
import json

# Variables
fill_names = ["A0", "B1", "C2", "D3", "E4", "F5", "G6", "H7", "I8", "J9"]
value_range = (1, 20000)
number_range = (1, 5000)


# url controll server
URL = "http://127.0.0.1:6003/stocks"


async def send_stocks():
    name = random.choice(fill_names)
    value = round(random.uniform(1, 20000), 2)
    number = random.randint(number_range[0], number_range[1])
    data = {'name': name, 'price': value, 'number': number}
    response = requests.post(URL, data=json.dumps(data))
    return data, response

async def task():
    """ Task execute send method """
    try:
        # Print time
        print(F"Time: {round(time.time() - start_time, 1)}") 
        
        # Generate and send stocks
        data = await send_stocks()

        print(F"Buy {data[0]} | Status code: {data[1]}")
    except Exception as err:
        print("Wait for connection")


async def do_task_periodically(interval, task):

    """ Loop task every interval in seconds. """
    while True:
        await asyncio.gather(
            asyncio.sleep(math.ceil(random.randint(1, interval))),
            task(),
        )


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(do_task_periodically(5, task))
