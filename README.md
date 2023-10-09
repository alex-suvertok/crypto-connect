# Crypto Exchange Information Fetcher

This Django project includes management commands to fetch information from crypto exchanges such as Binance and BingX. You can use these commands to retrieve account balances and current exchange rates for specific currency pairs.

## Installation

1. Clone the repository.
2. Install Dependencies: Install the required libraries and packages into your environment using the requirements.txt file. Run the following command: `pip install -r requirements.txt`  
3. Configure API keys for your crypto exchanges. You can do this by specifying the API keys as command line arguments when running the management commands.

## Usage

### `simple_exchange_info` Command

The `simple_exchange_info` command uses the `ccxt` library to fetch crypto exchange information and is designed for connecting to exchanges like Binance and BingX. This command simplifies the integration process and provides flexibility for adding more exchange support in the future.

To fetch information from Binance and BingX using the `simple_exchange_info` command, use the following management command:

```python3 manage.py simple_exchange_info --api-key-binance=XXX --api-secret-key-binance=YYY --api-key-bingx=ZZZ --api-secret-key-bingx=WWW```

This command leverages the `ccxt` library to connect to the specified exchanges. You can extend the code to support additional exchanges if needed.


### `exchange_info` Command

The `exchange_info` command allows you to fetch crypto exchange information without using external libraries that connect to cryptocurrency exchanges directly. It provides a starting point for implementing custom exchange integrations. 

To fetch information from Binance using the `exchange_info` command, use the following management command:

```python3 manage.py exchange_info --api-key-binance=XXX --api-secret-key-binance=YYY```

You can also specify additional options such as currency pairs using the `--currency-pairs` argument.
If the `--currency-pairs` option is not specified, 2 currency pairs BTC/USDT and ETH/USDT will be displayed.


## Example Output

### exchange_info
1. `python3 manage.py exchange_info --api-key-binance=XXX --api-secret-key-binance=YYY`  
```
Waiting for your "Binance" account balance and current rates...
Currency pairs: BTCUSDT, ETHUSDT

Current rates:
BTCUSDT: 27535.13
ETHUSDT: 1596.41

List of balances:
BTC: 0.00012382
ETH: 0.01704918
USDT: 1.0
MATIC: 1.981
LDBNB: 0.01043186
LDBTC: 0.00099839
APE: 0.40481061
LDAPE: 1.89136314
RDNT: 0.01761263
SUI: 0.01689775
MAV: 0.02280606
PENDLE: 0.00461458
CYBER: 0.0033659
SEI: 0.16511031
```

2. `python3 manage.py exchange_info --api-key-binance=XXX --api-secret-key-binance=YYY --currency-pairs bnb-Usdt test-2-usd`  
```
Waiting for your "Binance" account balance and current rates...
Currency pairs: BNBUSDT, TEST2USD

List of balances:
BTC: 0.00012382
ETH: 0.01704918
USDT: 1.0
MATIC: 1.981
LDBNB: 0.01043186
LDBTC: 0.00099839
APE: 0.40481061
LDAPE: 1.89136314
RDNT: 0.01761263
SUI: 0.01689775
MAV: 0.02280606
PENDLE: 0.00461458
CYBER: 0.0033659
SEI: 0.16511031

Current rates:
BNBUSDT: 208.2

No rate found:
TEST2USD
```

3. `python3 manage.py exchange_info --api-key-binance=XXX --api-secret-key-binance=YYY --currency-pairs BNB/USDT`  
```
Waiting for your "Binance" account balance and current rates...
Currency pairs: BNBUSDT

List of balances:
BTC: 0.00012382
ETH: 0.01704918
USDT: 1.0
MATIC: 1.981
LDBNB: 0.01043186
LDBTC: 0.00099839
APE: 0.40481061
LDAPE: 1.89136314
RDNT: 0.01761263
SUI: 0.01689775
MAV: 0.02280606
PENDLE: 0.00461458
CYBER: 0.0033659
SEI: 0.16511031

Current rates:
BNBUSDT: 208.0
```

### simple_exchange_info

1. `./manage.py simple_exchange_info --api-key-binance=XXX --api-secret-key-binance=YYY`
```
Platform: binance

List of balances:
BTC: 0.00012382
ETH: 0.01704918
USDT: 1.0
MATIC: 18.981
LDBNB: 0.01043186
LDBTC: 0.00099839
APE: 0.40481061
LDAPE: 1.89136314
RDNT: 0.01761263
SUI: 0.01689775
MAV: 0.02280606
PENDLE: 0.00461458
CYBER: 0.0033659
SEI: 0.16511031

Current prices:
BTC/USDT: 27512.84
ETH/USDT: 1594.5
```

2. `./manage.py simple_exchange_info --api-key-bingx=XXX --api-secret-key-bingx=YYY`  
```
Platform: bingx

List of balances:
USDT: 10.0

Current prices:
BTC/USDT: 27512.84
ETH/USDT: 1594.5
 ```