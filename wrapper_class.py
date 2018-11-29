from ibapi.wrapper import EWrapper  # used to handle the feedback information form the client
# from ibapi.client import EClient    # be responsibility for communication between the wrapper and client
from ibapi.contract import * # used to handle the characteristics of a stock, available when searching a stock
from ibapi.ticktype import *
from strategy import *
from ibapi.decoder import *
import datetime


class app_client(EWrapper, EClient):
    def __init__(self, contract: Contract, account: str):
        EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        self.next_orderID = 0                               # 下一个订单orderID
        self.contract = contract
        self.my_strategy_order = strategy_order(contract)
        self.account = account                              # 用来接收账户名称

        self.long_or_short = 0                              # 初始持仓的多空方向，1多头，-1空头，0空仓

        self.long_or_short_ready = False                        # 当前持仓状态是否更新完毕标志位，完毕为1，没完毕为0
        self.lastOrderDone = True                              # 上一个订单已经成交标志位，为1表示上一订单已成交
        self.orderID_ready = True                              # 为1表示orderId已经申请成功

        # self.last_value_0 = False                           # 存储上一个周期的delay数据
        # self.delay_done = False                             # delay是否完成

        self.last_price_time = datetime.datetime.now()            # 上一次刷新价格时间


    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        # EWrapper.error(self, reqId, errorCode, errorString)
        print("Error", reqId, errorCode, errorString)

        # 发生错误时，若干周期内不准交易
        self.my_strategy_order.current_cycles = 5
        self.my_strategy_order.cycles_ok = 0







    def position(self, account: str, contract: Contract, position: float, avgCost: float):
        EWrapper.position(self, account, contract, position, avgCost)
        print("Position.", account, "Symbol:", contract.symbol, "SecType:",
          contract.secType, "Currency:", contract.currency,
          "Position:", position, "Avg cost:", avgCost)
        # print("hahahahah")


        if contract.symbol == self.contract.symbol and contract.currency == self.contract.currency:
            if position > 0:
                self.long_or_short = 1
            elif position < 0:
                self.long_or_short = -1
            else:
                self.long_or_short = 0

        self.long_or_short_ready = True



    def nextValidId(self, orderId:int):
        EWrapper.nextValidId(self, orderId)
        self.next_orderID = orderId
        self.orderID_ready = True
        # print("orderID:", orderId)



    def orderStatus(self, orderId:OrderId , status:str, filled:float,
                    remaining:float, avgFillPrice:float, permId:int,
                    parentId:int, lastFillPrice:float, clientId:int,
                    whyHeld:str):
        EWrapper.orderStatus(self, orderId, status, filled, remaining,
                            avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld)

        if status == "Filled":
            self.lastOrderDone = True
        # print(status)



    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        super().openOrder(orderId, contract, order, orderState)
        self.lastOrderDone = False



    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float, attrib: TickAttrib):
        EWrapper.tickPrice(self, reqId, tickType, price, attrib)
        # print("tickPrice:", price)
        # print("long_or_short_ready: ", self.long_or_short_ready)
        # 跳过前N个周期
        self.my_strategy_order.skip_first_N_cycles()
        # 判断delay是否完成
        now = datetime.datetime.now()
        # print( now - self.last_price_time)
        if now - self.last_price_time > datetime.timedelta(seconds=10):
            delay_done = True
            self.last_price_time = now
            # print(now)
            # 更新指标周期
            self.my_strategy_order.index_18.update_last_wiMA()
            self.my_strategy_order.index_25.update_last_wiMA()
        else:
            delay_done = False



        # 当账户信息更新完毕后，上一订单完成后，orderId准备好后，延时有效之后，开始执行策略
        if self.lastOrderDone and self.orderID_ready and self.long_or_short_ready and delay_done:
            # 测试信号
            # print("tickPrice:", price)
            # 关断上一订单已完成标志位
            self.lastOrderDone = False
            # 将持仓状态数据传入策略
            self.my_strategy_order.get_current_state(self.long_or_short)
            # 关断持仓状态可读标志位
            self.long_or_short_ready = False


            # 将价格数据和持仓状态数据传入策略
            self.my_strategy_order.get_price(price)
            # 执行策略分析，返回决策结果
            order_contract, order_order = self.my_strategy_order.strategy_exe()
            # 执行策略
            if order_contract != "hold":
                self.placeOrder(self.next_orderID, order_contract, order_order)
                # print(self.next_orderID)
                # 关断orderId可用标志位
                self.orderID_ready = False
                # 申请orderID
                self.reqIds(0)
            else:
                # print("do nothing")
                self.lastOrderDone = True
                self.long_or_short_ready = True




        # 调取时间信息，根据时间情况来更新指标曲线
        # print(time.localtime())

    def tickSize(self, reqId:TickerId, tickType:TickType, size:int):
        super().tickSize(reqId, tickType, size)
        # print("exe tickSize")
        # print("size", size)

    def tickReqParams(self, tickerId: int, minTick: float, bboExchange:str, snapshotPermissions: int):
        super().tickReqParams(tickerId, minTick, bboExchange, snapshotPermissions)
        print("tickReqParams: ", tickerId, " minTick: ", minTick," bboExchange: ", bboExchange, " snapshotPermissions: ", snapshotPermissions)

    def tickString(self, reqId:TickerId, tickType:TickType, value:str):
        super().tickString(reqId, tickType, value)
        print("exe tickString")
        print("tickType, value:", tickType, value)

    def tickGeneric(self, reqId: TickerId, tickType: TickType, value: float):
        super().tickGeneric(reqId, tickType, value)
        print("exe tickgeneric")
        print("Tick Generic. Ticker Id:", reqId, "tickType:", tickType, "Value:", value)