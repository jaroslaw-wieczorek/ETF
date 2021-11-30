from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
import logging

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
        "A0": 0,
        "B1": 0,
        "sum":0,
        "percent": 0.0,
        "target_percent": 0.41,
    },
    "user2": {
        "A0": 0,
        "B1": 0,
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
            wallets[user]['sum'] = 0
            wallets[user]['percent'] = 0
            wallets[user]['target_percent'] = target_percents[user]
            for stock in stock_prices:
                wallets[user][stock] = 0


def update_stock_price(stock_name: str, stock_price: int):
    """ Update stocks prices """

    if stock_name not in stock_prices:
        stock_prices[stock_name] = {}
        stock_prices[stock_name]['old'] = stock_price
        stock_prices[stock_name]['new'] = stock_price

        for user in wallets:
            wallets[user][stock_name] = 0
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
            if stock_name not in wallets[user]:
                wallets[user][stock_name] = 0
            
            num = wallets[user][stock_name]
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


def spread_stocks_to_wallets(stock_name, stock_number, stock_price):
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
        wallets[target_wallet][stock_name] += stock_number
        wallets[target_wallet]['percent'] += stock_percent
        wallets[target_wallet]['sum'] += stock_value

    else:
        for i in range(stock_number):
            wallets[target_wallet][stock_name] += 1
            wallets[target_wallet]['sum'] += stock_price
            target_wallet, target_demand = choose_target_wallet()


app.post("stocks/")
def get_new_stock(stock: dict):
    """ Handling of new stocks """ 
    stock_name = stock['name']
    stock_price = stock['price']
    stock_number = stock['number']
        
    if stock_price < 0 or int(stock_number) < 1:
        # Wrong data 
        return 1

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

    # print(F"Stock value: {stock_value}")
    # print(F"Stock percent (value/total_sum + value): {stock_percent}")

    # Spread stocks
    spread_stocks_to_wallets(
        stock_name=stock_name, 
        stock_number=stock_number, 
        stock_price=stock_price
    )

    return wallets


# def test(test_stock):
#     print(F"Wallets: {wallets}")
#     print(F"wallets_balance: {wallets_balance}")
#     get_new_stock({"name": "A0", "number": 29, "price": 10})
#     print()

#     print(F"Wallets: {wallets}")
#     print(F"wallets_balance: {wallets_balance}")
#     get_new_stock({"name": "A0", "number": 10, "price": 100})
#     print()

#     print(F"Wallets: {wallets}")
#     print(F"wallets_balance: {wallets_balance}")
#     print()

#     balance = {"user1": 0.34, "user2": 0.50, "user3": 0.16}
#     print(f"Update wallet balance! ==|> {balance}") 
#     get_new_target_percents(balance)

#     print(F"Wallets: {wallets}")
#     print(F"wallets_balance: {wallets_balance}")
#     get_new_stock({"name": "A0", "number": 300, "price": 100})

#     print(F"Wallets: {wallets}")
#     print(F"wallets_balance: {wallets_balance}")
#     get_new_stock({"name": "A0", "number": 30000, "price": 2100})

#     tmp_sum = 0
#     for user in wallets:
#         tmp_sum += wallets[user]['percent']
#     print(tmp_sum)


@app.post("/aum")
async def getConfAUM(data : Request):
    req_data = await data.json()
    get_new_target_percents(req_data)
    for user in wallets:
        print(f"{user} - {round(wallets[user]['percent'], 3)}:")
        print(f"\t new set - {wallets[user]['target_percent']}")
    return wallets


@app.post("/stocks")
async def getFillData(data : Request):
    req_data = await data.json()
    get_new_stock(req_data)
    for user in wallets:
        print(f"{user} - {round(wallets[user]['percent'], 3)}:")
        for stock in stock_prices:
            print(f"\t{stock}: {wallets[user][stock]}")
    return wallets


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=6003)
