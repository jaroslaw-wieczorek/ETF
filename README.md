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
\[\*\] New target balance for "user1" => 65.0</br>
\[\*\] New target balance for "user2" => 35.0</br>
INFO:&emsp127.0.0.1:37862 - "POST /aum HTTP/1.1" 200 OK</br>


### Example logs after got request from fill_server.py:
\[\*\] user1 | Sum: 1364116361.8697963 | Target balance:0.41 | Current balance:0.4100001345426599</br>
\[\*\] user2 | Sum: 1962995624.060422 | Target balance:0.59 | Current balance:0.5899998654574058</br>
INFO:&emsp127.0.0.1:37792 - "POST /stocks HTTP/1.1" 200 OK</br>


## Run aum server
python aum_server.py
### Example logs:
Time: 0.0</br>
Send data: {'user1': 67.0, 'user2': 33.0} | Status code: 200</br>
Time: 30.0</br>
Send data: {'user1': 64.0, 'user2': 36.0} | Status code: 200</br>


## Run fill server 
python fill_server.py

### Example logs from fill_server.py:
\[\*\] Time is seconds: 0.0</br>
\[\*\] Buy: {'name': 'G6', 'price': 9439.2, 'number': 67} | Status code: 200</br>
\[\*\] Response wallets status: {'user1': {'stocks': {'A0': 0, 'B1': 0, 'G6': 27}, 'sum': 254858.40000000014, 'percent': 0.4029850746268659, 'target_percent': 0.41}, 'user2': {'stocks': {'A0': 0, 'B1': 0, 'G6': 40}, 'sum': 377568.0000000003, 'percent': 0.5970149253731347, 'target_percent': 0.59}}</br>

\[\*\] Time is seconds: 5.0</br>
\[\*\] Buy: {'name': 'E4', 'price': 5662.35, 'number': 2396} | Status code: 200</br>
\[\*\] Response wallets status: {'user1': {'stocks': {'A0': 0, 'B1': 0, 'G6': 27, 'E4': 2396}, 'sum': 13821849.000000002, 'percent': 0.9734096125214154, 'target_percent': 50.0}, 'user2': {'stocks': {'A0': 0, 'B1': 0, 'G6': 40, 'E4': 0}, 'sum': 377568.0000000003, 'percent': 0.026590387478584526, 'target_percent': 41.0}, 'user3': {'stocks': {'A0': 0, 'B1': 0, 'G6': 0, 'E4': 0}, 'sum': 0, 'percent': 0.0, 'target_percent': 9.0}}</br>

## Wallet names (add next wallet after 3 sended sets) 
["user1", "user2", "user3", "user4", "user5", "user6", "user7"]

## Stocks names
["A0", "B1", "C2", "D3", "E4", "F5", "G6", "H7", "I8", "J9"]





