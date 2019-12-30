#!/usr/bin/python3

import requests
import os
import json
import alpaca_trade_api as tradeapi

from keys import *

# API paths
BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "/v2/account"
ORDERS_URL = "/v2/orders"
ACTIVITIES_URL = "/v2/account/activities"
POSITIONS_URL = "/v2/positions"
ASSET_URL = "/v2/assets"


MARKET_DATA_URL = "https://data.alpaca.markets/v1"

BARS_URL = "/bars/"

def main():
    pass

# returns current account information
def getAccount():
    return requests.get(BASE_URL + ACCOUNT_URL, headers=HEADERS)


# creates buy/sell order
def makeOrder(symbol, quantity, side, orderType="market", timeInForce="gtc", limitPrice=0, stopPrice=0):

    # set parameters
    order = {
        "symbol" : symbol,
        "qty" : quantity,
        "side" : side,
        "type" : orderType,
        "time_in_force" : timeInForce
    }

    # extra parameters if required
    if (orderType == "limit" or orderType == "stop_limit"):
        order["limit_price"] = limitPrice

    if (orderType == "stop" or orderType == "stop_limit"):
        order["stop_price"] = stopPrice




    return requests.post(BASE_URL + ORDERS_URL, json=order, headers=HEADERS).json()


# get all current orders
def getOrders():
    return requests.get(BASE_URL + ACCOUNT_URL, headers=HEADERS).json()
        

# get all avaliable stocks
def getAllAssets():
    return requests.get(BASE_URL + ASSET_URL, headers=HEADERS).json()


# get specific stock information
def getAsset(symbol):
    return requests.get(BASE_URL + ASSET_URL + "/" + symbol, headers=HEADERS).json()


# trade information of this account for the stock
def getPosition(symbol):
    return requests.get(BASE_URL + POSITIONS_URL + "/" + symbol, headers=HEADERS).json()


# get market data for a stock
def getMarketData(timeframe, symbols, limit, start, end, after, until):
    # set parameters

    parameters = {
        "symbols" : ["AAPL"]
        # "limit" : limit,
        # "start" : start,
        # "end" : end,
        # "after" : after,
        # "until" : until
    }
    return requests.get("https://data.alpaca.markets/v1/bars/" + timeframe, json=parameters, headers=HEADERS)



if __name__ == '__main__':
    print("STARTING!")
    os.environ["APCA_API_KEY_ID"] = KEY_ID
    os.environ["APCA_API_SECRET_KEY"] = SECRET_KEY
    api = tradeapi.REST()

    result = api.get_barset('AAPL', 'day', limit=5)

    

    exit()
    stock = "AAPL"
    asset = getAsset(stock)
    position = getPosition(stock)
    print (asset)
    print(position)

    print ("====================")
    marketData = getMarketData("day", stock, 100, "2019-04-15T09:30:00-04:00",  '2019-04-15T10:30:00-04:00', "", "")    
    print(marketData.content)
