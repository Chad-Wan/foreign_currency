from ibapi.order import *


def limitOrder(action: str, quantity: float, limitPrice: float):
    order = Order()
    order.action = action
    order.orderType = "LMT"
    order.totalQuantity = quantity
    order.lmtPrice = limitPrice
    order.transmit = True
    return order


def marketOrder(action: str, quantity: float):
    order = Order()
    order.action = action
    order.orderType = "MKT"
    order.totalQuantity = quantity
    order.transmit = True
    return order


def stopOrder(action: str, quantity: float, stopPrice: float):
    order = Order()
    order.action = action
    order.orderType = "STP"
    order.auxPrice = stopPrice
    order.totalQuantity = quantity
    order.transmit = True
    return order


def stopLimitOrder(action: str, quantity: float, limitPrice: float, stopPrice: float):
    order = Order()
    order.action = action
    order.orderType = "STP LMT"
    order.totalQuantity = quantity
    order.lmtPrice = limitPrice
    order.auxPrice = stopPrice
    order.transmit = True
    return order


def trailingStop(action: str, quantity: float, trailingPercent: float,
                     trailStopPrice: float):
    order = Order()
    order.action = action
    order.orderType = "TRAIL"
    order.totalQuantity = quantity
    order.trailingPercent = trailingPercent
    order.trailStopPrice = trailStopPrice
    order.transmit = True
    return order
