import requests
import pymongo

API_URL = 'https://api.coinmarketcap.com/v2/ticker/' # API address

def get_db_conection(uri): # Varible uri = Mongo server address
    client = pymongo.MongoClient(uri) # Create Client in MongoDB
    return client.cryptongo

def get_cryptocurrencies_from_api():
    r = requests.get(API_URL) # Get API result

    if r.statud_code == 200: # Verify if the code state is the one that is needed
        result = r.json() # Convert information to Json
        return result
    
    raise Exception('API Error') # raise = Create error

def get_hash(value):
    from hashlib import sha512
    return sha512(value.encode('utf-8')).hexdigest()

def first_element(elements):
    return elements [0]

def get_ticker_hash(ticker_data):
    from collections import OrdereDict
    ticker_data = OrdereDict(
        sorted(
            ticker_data.items(),
            key = first_element

            )
        )

    ticker_value = ''

    for _, value in ticker_data.items():
        ticker_value += str(value)

    return get_hash(ticker_value)

def check_if_exists(db_coneccion, ticker_data):
    ticker_hash = get_ticker_hash(ticker_data)
    if db_coneccion.tickers.find_one({'ticker_hash': ticker_hash}): # If exist into Database, return True
        return True

    return False

def save_ticker(db_coneccion, ticker_data = None):
    if not ticker_data:
        return False
    
    if check_if_exists(db_coneccion, ticker_data): # If the function return true, then cancel process
        return False

    ticker_hash = get_ticker_hash(ticker_data)
    ticker_data['ticker_hash'] = ticker_hash
    ticker_data['rank'] = int(ticker_data['rank']) # Get values and Convert to int
    ticker_data['last_updated'] = int(ticker_data['last_updated'])

    db_coneccion.tickers.insert_one(ticker_data) # Insert all ticket information
    return True

if __name__ == '__main__':