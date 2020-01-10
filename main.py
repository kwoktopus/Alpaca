#!/usr/bin/python3

import requests
import os
import json
import alpaca_trade_api as tradeapi

from keys import *
import watchlist
from marketData import Market


# API paths
BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "/v2/account"
ORDERS_URL = "/v2/orders"
ACTIVITIES_URL = "/v2/account/activities"
POSITIONS_URL = "/v2/positions"
ASSET_URL = "/v2/assets"


MARKET_DATA_URL = "https://data.alpaca.markets/v1"
BARS_URL = "/bars/"

CAPACITY = 300

def main():
    api = tradeapi.REST(KEY_ID, SECRET_KEY, api_version='v2')
    market = Market(api)

    market.watchList = watchlist.stocks

    maxDiff = 0
    bestStock = None

    print (len(market.watchList))
    n = 0

    positions = {}
    for position in api.list_positions():
        positions[position.symbol] = position.qty
    
 
    # api.submit_order("AAPL", 1000, 'buy', 'market', 'day')

    results = []

    for stock in market.watchList[:10]:

        timeframe = "5Min"


        # if moving average of shorter period > moving average of higher period we should buy. Otherwise sell.

        lower = market.getMovingAverage(stock, timeframe, 50)
        upper = market.getMovingAverage(stock, timeframe, 200)


        results.append((stock, (upper - lower)/((lower + upper)/2)))

    results.sort(key=lambda x : x[1])
    
    for result in results:
        try:
            if (result[1] < 0): # sellable
                amount = positions[result[0]]
                if (amount):
                    api.submit_order(result[0], amount, "sell", 'market', 'day')
            else:
                break

        except Exception:
            pass

    for result in reversed(results):
        try:
            if (result[1] > 0): # buyable
                cost = api.get_barset(result[0], "1Min", limit = 1)[result[0]][0].o
                api.submit_order(result[0], 500//int(cost), "buy", 'market', 'day')
            else:
                break

        except Exception:
            print ("not enough buying power")
            break



    # for asset in api.list_assets():
    #     if asset.tradable and asset.easy_to_borrow and asset.status == 'active':
    #         market.addWatchList(asset.symbol)
    
    
    


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
    main()

    # os.environ["APCA_API_KEY_ID"] = KEY_ID
    # os.environ["APCA_API_SECRET_KEY"] = SECRET_KEY

    # api = tradeapi.REST(KEY_ID, SECRET_KEY, api_version='v2')

    # stocks = ["MSFT"]
    
    # marketData = MarketData(api)

    
    # print ("====================")
    # while (True):
    #     for stock in stocks:    
            
            
    #         nShares = 0
    #         for position in api.list_positions():
    #             if position.symbol == stock:
    #                 nShares = int(position.qty)
    #                 break
        
    #         nOrders = 0
    #         for order in api.list_orders():
    #             if order.symbol == stock and order.side == "buy":
    #                 nOrders = int(order.qty)
    #                 break

    #         # don't buy over capacity
    #         if (nShares + nOrders >= CAPACITY):
    #             break

    #         avg200 = 0
    #         avg50 = 0

    #         bar200 = api.get_barset(stock, '15Min', limit=200)[stock]
    #         bar50 = api.get_barset(stock, '15Min', limit=50)[stock]

    #         for bar in bar200:
    #             avg200 += bar.o

    #         for bar in bar50:
    #             avg50 += bar.o

    #         avg200 /= 200
    #         avg50 /= 50

    #         print ("avg50 =",avg50, "avg200 =", avg200)

    #         if avg50 > avg200:
    #             # buy
    #             amount = CAPACITY - nShares - nOrders
                
    #             price = api.get_barset(stock, '1Min', 1)[stock][0].o
    #             buyingPower = api.get_account().daytrading_buying_power
    #             if (amount * price > buyingPower): # if we don't have enough funds
    #                 amount = buyingPower / price


    #             print ("buying", CAPACITY - nShares - nOrders)
    #             api.submit_order(stock, CAPACITY - nShares - nOrders, 'buy', 'market', 'day')
            

    #         if avg50 < avg200 and nShares > 0: # sell
    #             print ("selling", nShares)
    #             api.submit_order(stock, nShares, 'sell', 'market', 'day')

