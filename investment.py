from ibapi.contract import *

def EUR_JPY():
    contract = Contract()
    contract.symbol = "EUR"
    contract.secType = "CASH"
    contract.currency = "JPY"
    contract.exchange = "IDEALPRO"
    return contract

def EUR_USD():
    contract = Contract()
    contract.symbol = "EUR"
    contract.secType = "CASH"
    contract.currency = "USD"
    contract.exchange = "IDEALPRO"
    return contract

def USD_JPY():
    contract = Contract()
    contract.symbol = "USD"
    contract.secType = "CASH"
    contract.currency = "JPY"
    contract.exchange = "IDEALPRO"
    return contract

def GBP_USD():
    contract = Contract()
    contract.symbol = "GBP"
    contract.secType = "CASH"
    contract.currency = "USD"
    contract.exchange = "IDEALPRO"
    return contract