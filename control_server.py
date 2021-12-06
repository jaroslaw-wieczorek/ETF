from fastapi import FastAPI, Request, Body
from pydantic import BaseModel
from fastapi import HTTPException, status

import uvicorn
import logging
import json
from fastapi.encoders import jsonable_encoder
from fastapi.openapi.utils import get_openapi

LOGGING_FORMAT = '[%(asctime)s] [%(levelname)s] %(message)s'
logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO)

app = FastAPI()
app.secret = "fsjosfdjosjfosjdf"


# Accout names in first tick
account_names = ["user1", "user2"]

# Stock prices
stock_prices = {
    "A0": {"old": 0, "new": 0},
    "B1": {"old": 0, "new": 0}
}

# Users accounts/wallets
wallets = {
    "user1": {
        "stocks": {
            "A0": 0,
            "B1": 0,
        },
        "sum":0,
        "percent": 0.0,
        "target_percent": 0.41,
    },
    "user2": {
        "stocks": {
            "A0": 0,
            "B1": 0,
        },
        "sum":0,
        "percent": 0.0,
        "target_percent": 0.59,
    }
}

# Total balance
wallets_balance = {
    "total_sum": 0
}


def get_new_target_percents(target_percents: dict):
    """ Update target percent for wallets"""

    for user in target_percents:
        if user in wallets:
            wallets[user]['target_percent'] = target_percents[user]
        else:
            wallets[user] = {}
            wallets[user]['stocks'] = {}
            wallets[user]['sum'] = 0
            wallets[user]['percent'] = 0
            wallets[user]['target_percent'] = target_percents[user]
            for stock in stock_prices:
                wallets[user]['stocks'][stock] = 0


def update_stock_price(stock_name: str, stock_price: int):
    """ Update stocks prices """

    if stock_name not in stock_prices:
        stock_prices[stock_name] = {}
        stock_prices[stock_name]['old'] = stock_price
        stock_prices[stock_name]['new'] = stock_price

        for user in wallets:
            wallets[user]['stocks'][stock_name] = 0
    else:
        stock_prices[stock_name]['old'] = stock_prices[stock_name]['new']
        stock_prices[stock_name]['new'] = stock_price

    if stock_prices[stock_name]['old'] != stock_prices[stock_name]['new']:
        # required update the wallets values 
        return 1

    # dosen't required update the wallets values 
    return 0


def update_total_sum():
    """ Update total sum """
    wallets['total_sum'] = 0
    for user in wallets:
        wallets['total_sum'] += wallets[user]['sum']


def update_users_wallets(stock_name: str):
    """ Update user wallets """

    # Get stock prices (stock)
    old_price = stock_prices[stock_name]['old']
    new_price = stock_prices[stock_name]['new']

    # Update wallet 
    if stock_name and stock_name not in ['sum', 'percent']:
        for user in wallets:
            if stock_name not in wallets[user]['stocks']:
                wallets[user]['stocks'][stock_name] = 0
            
            num = wallets[user]['stocks'][stock_name]
            if num > 0:
                # Count difference  
                value_diff = (new_price * num) - (old_price * num)

                # Update wallet value (value of current user) 
                wallets[user]['sum'] += value_diff

                # Update total_sum (value of all wallets)
                wallets_balance['total_sum'] += value_diff

    if wallets_balance['total_sum'] > 0:
        for user in wallets:
            wallets[user]['percent'] = wallets[user]['sum'] / wallets_balance['total_sum']


def choose_target_wallet():
    """ Choose target wallet """
    total_sum = wallets_balance['total_sum']
    target_demand = 0
    target_wallet = ''
    for user in wallets:
        wallets[user]['percent'] = wallets[user]['sum'] / total_sum

        if wallets[user]['target_percent'] -  wallets[user]['percent'] > target_demand:
            target_demand = wallets[user]['target_percent'] -  wallets[user]['percent']
            target_wallet = user

    return target_wallet, target_demand


def spread_stocks_to_wallets(stock_name: str, stock_number: int, stock_price: float):
    """ Divide stocks between wallets """
    stock_value = stock_number * stock_price
    stock_percent = 0

    target_wallet = ''
    target_demand = 0

    # Change total sum (add new stock value)
    wallets_balance['total_sum'] += stock_value

    # Calculate stock percent / total stocks in wallets
    stock_percent = stock_value / wallets_balance['total_sum']

    # Calculation of the new percentage distribution of wallets 
    # (taking into account the value of new stocks)
    target_wallet, target_demand = choose_target_wallet()

    if target_demand >= stock_percent:
        wallets[target_wallet]['stocks'][stock_name] += stock_number
        wallets[target_wallet]['percent'] += stock_percent
        wallets[target_wallet]['sum'] += stock_value

    else:
        for i in range(stock_number):
            wallets[target_wallet]['stocks'][stock_name] += 1
            wallets[target_wallet]['sum'] += stock_price
            target_wallet, target_demand = choose_target_wallet()


def get_new_stock(stock: dict) -> dict:
      
    stock_name = stock['name']
    stock_price = stock['price']
    stock_number = stock['number']
   
    # Update stock price
    update = update_stock_price(stock_name=stock_name, stock_price=stock_price)

    # If the price of stock 'X' has changed since the last time the values
    # of the wallets that hold it should be updated.
    if update:
        # Update wallet prices and percent (before split new stock)
        update_users_wallets(stock_name=stock_name)

    # Calculating how much percentage of the value of all wallets is currently
    # received shares.
    stock_value = stock_price * stock_number
    stock_percent = stock_value / (wallets_balance['total_sum'] + stock_value)

    # Spread stocks
    spread_stocks_to_wallets(
        stock_name=stock_name, 
        stock_number=stock_number, 
        stock_price=stock_price
    )

    return wallets

@app.get("/wallets", status_code=status.HTTP_200_OK, response_model=dict)
async def get_current_aum_conf() -> dict:
    """
    Return current wallets data
    """
    return wallets


@app.post("/aum", status_code=status.HTTP_200_OK, response_model=dict)
async def post_new_aum_conf(data: Request) -> dict:
    """
    Set new wallets balance
        
    Responses:
      200: ok
      400: Bad request

    Body:
        {"user1": 55, "user2": 45"}
    """
    
    aum_data = await data.json()
    
    if not isinstance(aum_data, dict) or not all(key in aum_data.keys() for key in account_names):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=F"Forget about someone account balance"
        )

    if any((type(v) not in [int, float] or v <= 0) for v in aum_data.values()) or sum(aum_data.values()) != 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=F"The value for each account must be greater than zero!"
        )

    get_new_target_percents(aum_data)
    for user in wallets:
        print(f"[*] New target balance for \"{user}\" => {wallets[user]['target_percent']}")
    return wallets


@app.post("/stocks", status_code=status.HTTP_200_OK)
async def post_new_stocks(data : Request) -> dict:
    """ Handling of new stocks 
     Responses:
      200: ok
      400: Bad request

    Body:
        {"name": "A1", "price": 45.0, "number": 40}

    """  
    stock = await data.json()
    if not isinstance(stock, dict) or not all(key in stock.keys() for key in ["name", "price", "number"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="[!] Required keys in dict: \"name\" type str, \"price\" type float and \"number\" type int."
        )

    elif not isinstance(stock['price'], float) and not isinstance(stock['price'], int) or not isinstance(stock['number'], int) \
        or not isinstance(stock['name'], str) or float(stock['price']) <= 0 or int(stock['number']) <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="[!] Values \"price\" and \"number\" must be bigger than 0, \"name\" must be string."
        )    

    get_new_stock(stock)
    for user in wallets:
        print(f"[*] {user} | Sum: {wallets[user]['sum']} | Target balance:{wallets[user]['target_percent']} | Current balance:{wallets[user]['percent']}")
    return wallets


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=6003)
