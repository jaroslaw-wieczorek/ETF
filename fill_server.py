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
    """ Generate and send new stock """
    global URL
    name = str(random.choice(fill_names))
    value = float(round(random.uniform(1, 20000), 2))
    number = random.randint(number_range[0], number_range[1])
    data = {'name': name, 'price': value, 'number': number}
    response = requests.post(url=URL, data=json.dumps(data))
    return data, response

async def task():
    """ Task execute send method """
    try:
        # Print time
        print(F"[*] Time is seconds: {round(time.time() - start_time, 1)}") 
        
        # Generate and send stocks
        data, r = await send_stocks()
        print(F"[*] Buy: {data} | Status code: {r.status_code}")
        if r.status_code != 200:
            print(F"[!] {r.content.decode('utf-8')}\n")
        else:
            print(F"[*] Response wallets status: {r.json()}\n")
    except requests.exceptions.ConnectionError as err:
        print("[!] Wait for connection")
        counter = 0
    except Exception as err:
        print(F"[!] Error: {err}")
        counter = 0


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
