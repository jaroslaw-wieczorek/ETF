# ETF
Example of a simple system that divides stocks between wallets according to a given percentage distribution.  
## Repository contains 3 scripts: 

  ### fill_server.py
    Simulates server which sends stocks to divide between wallets ex.: {"name": "A0", "number": 100, "price": 440}
  ### aum_server.py
    Simulates a server sending the balance of wallets ex.: {"user1": 0.51, "user2": 40, "user3": 9}
  ### control_server.py 
    FastAPI simple server. Listens on port 6003 waits for data on two endpoints (/stocks -- for stocks, /aum -- for new wallet balance}


# How to run
## Preparation of the environment and required packages
pipenv shell</br>
pipenv install</br>

## Run control server
python control_server.py</br>

### Example logs after got request from aum_server.py:</br>
user1 - 0.0:</br>
&emsp;new set - 32.0</br>
user2 - 0.0:</br>
&emsp;new set - 68.0</br>
INFO:&emsp;127.0.0.1:48724 - "POST /aum HTTP/1.1" 200 OK

### Example logs after got request from fill_server.py:
user1 - 0.41:</br>
&emsp;A0: 0</br>
&emsp;B1: 0</br>
&emsp;C2: 1149</br>
&emsp;I8: 1530</br>
user2 - 0.59:</br>
&emsp;A0: 0</br>
&emsp;B1: 0</br>
&emsp;C2: 1653</br>
&emsp;I8: 2202</br>
INFO:&emsp;127.0.0.1:48772 - "POST /stocks HTTP/1.1" 200 OK


## Run aum server
python aum_server.py
### Example logs:
Time: 0.0</br>
Send data: {'user1': 67.0, 'user2': 33.0} | Status code: 200</br>
Time: 30.0</br>
Send data: {'user1': 64.0, 'user2': 36.0} | Status code: 200</br>


## Run fill server 
python fill_server.py

### Example logs:
Time: 0.0</br>
Buy {'name': 'C2', 'price': 2000.54, 'number': 2802} | Status code: <Response [200]></br>
Time: 3.0</br>
Buy {'name': 'I8', 'price': 16177.93, 'number': 3732} | Status code: <Response [200]></br>

## Wallet names (add next wallet after 3 sended sets) 
["user1", "user2", "user3", "user4", "user5", "user6", "user7"]

## Stocks names
["A0", "B1", "C2", "D3", "E4", "F5", "G6", "H7", "I8", "J9"]





