from fastapi import FastAPI, Request

import asyncio
import math
import random
import requests
import time
import json

# Create app
app = FastAPI()

# Account_names
account_names = ["user1", "user2", "user3", "user4", "user5", "user6", "user7"]

# Keep created user names
data = {}
counter = 0
account_num = 2

# Address of server
URL = "http://127.0.0.1:6003/aum"


def random_target_percent(parts, total=100, places=0):
    """Generate random seq that sum to 100"""

    a = []
    for n in range(parts):
        a.append(random.random())

    b = sum(a)
    c = [x/b for x in a]    
    d = sum(c)
    e = c

    if places is not None:
        e = [round(x * total, places) for x in c]

    f = e[-(parts-1):]
    g = total - sum(f)

    if places is not None:
        g = round(g, places)
    
    f.insert(0, g)
    return f   


def generate_data(account_num=2):
    """Generate accounts balance """

    # Chose names from list
    chosed_name = account_names[:account_num]

    # Split 100 between number of accounts
    f = random_target_percent(account_num)

    # Assign balance to account
    for account in account_names:
        if account in chosed_name:
            data[account] = f.pop()
    return data


async def send_new_wallets_balance():
    """ Send data to control server.py """
    global account_num, counter, URL

    # Simple increase number of accounts
    if account_num < 7:
        counter += 1
        if counter > 2:
            account_num += 1
            counter = 0

    # Generate data 
    data = generate_data(account_num)

    # Send post
    r = requests.post(url=URL, data=json.dumps(data))
    return data, r.status_code


async def task():
    """ Task execute send method """
    try:
    	# Print time
        print(F"Time: {round(time.time() - start_time, 1)}") 

        # Generate and send data
        data = await send_new_wallets_balance()
        print(F"Send data: {data[0]} | Status code: {data[1]}")
    except Exception as err:
        print("Wait for connection")


async def do_task_periodically(interval, task):

    """ Loop task every interval in seconds. """
    while True:
        await asyncio.gather(
            asyncio.sleep(interval),
            task(),
        )


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(do_task_periodically(30, task))
