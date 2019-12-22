import requests
import os
import json

from keys import *

HEADERS = {'APCA-API-KEY-ID':KEY_ID, 'APCA-API-SECRET-KEY':SECRET_KEY}

BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "/v2/account"
ORDERS_URL = "/v2/orders"
ACTIVITIES_URL = "/v2/account/activities/"
POSITIONS_URL = "/v2/positions"



def main():
	pass

def getAccount():
	return requests.get(BASE_URL + ACCOUNT_URL, headers=HEADERS)

def makeOrder(symbol, quantity, side, orderType="market", timeInForce="gtc", limitPrice="limit", stopPrice="stop"):

	order = {
		"symbol" : symbol,
		"qty" : quantity,
		"side" : side,
		"type" : orderType,
		"time_in_force" : timeInForce
	}

	if (orderType == "limit" or orderType == "stop_limit"):
		order["limit_price"] = limitPrice

	if (orderType == "stop" or orderType == "stop_limit"):
		order["stop_price"] = stopPrice




	return requests.post(BASE_URL + ORDERS_URL, json=order, headers=HEADERS)


def getOrders():
	return requests.get(BASE_URL + ACCOUNT_URL, headers=HEADERS)


if __name__ == '__main__':
	print("STARTING!")
	# makeOrder(symbol, quantity, side) , side = "buy" or "sell"
	