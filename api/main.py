import pymongo
from flask import Flask, jsonify, request # jsonify returns in json format
# Flask is to raise a web server
def get_db_connection(url): # Varible url = Mongo server address
    client = pymongo.MongoClient(url) # Create Client in MongoDB
    return client.cryptongo

app = Flask(__name__) # Create a web server
db_connection = get_db_connection('mongodb://localhost:27017/') # (Connection protocol URL://IP:Port/)

def get_document_and_top20(top = False): # Get the list of documents to return them
    params = {} # Data dictionary
    name = request.args.get('name', '') # Get name from GET, if it doesn't exist, then null
    limit = int(request.args.get('limit', 0)) # Get limit from method GET, if it dowsn't exist, then limit equals 0

    if name: params.update({'name': name}) # If the name exist, then add data dictionary
    if top: params.update({'rank': {'$lte': 20}}) # Show the first 20 in the ranking

    cursor = db_connection.tickers.find(params, {'_id': 0, 'ticker_hash': 0}).limit(limit)
    # Search for tickets as received from the GET method
    return list(cursor)

def remove_currency(): # Deleted Data
    params = {}
    name = request.args.get('name', name)
    
    if name: params.update({'name': name})
    else: return False
    # Delete all data that matches what the method received
    return db_connection.tickers.delete_many(params).deleted_count 
    
@app.route("/") # Define the route
def index():
    return jsonify({ 'name': 'Cryptongo API' })

@app.route("/tickers", methods=['GET', 'DELETE'])
def tickers():
    if request.method == 'GET': # If the method is GET, then execute this function
        return jsonify(get_document_and_top20())
    elif request.method == 'DELETE':
        result = remove_currency() # Else if the method is DELETE, then execute this function
        
        if result > 0: # If the result of deleting elements is greater than 0
            return jsonify({'text': 'Deleted document'}), 204 # FLASK allows you to add another parameter to the return
        else:
            return jsonify({'error': 'The documents do not exist'}), 404 # Answer from the http

@app.route("/top20", methods=['GET'])
def top20():
    return jsonify(get_document_and_top20(True))
