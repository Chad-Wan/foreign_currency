from order_class import *
from ibapi.client import *
import WiMA_index


class strategy_order():
    def __init__(self, input_contract: Contract, quantity = 20000):
        self.contract = input_contract
        self.quantity = quantity
        self.price = 0.0

        # 账户多空状态，1持有多头头寸，-1持有空头头寸，0空仓
        self.current_state = 0
        self.doNot_touch_currentState = 0

        # 双均线技术指标
        self.price_1 = 1.17460
        self.price_2 = 1.17430

        # 最初N个周期不准下单
        self.cancel_first_N_cycles = 15
        self.current_cycles = 1
        self.cycles_ok = 0

        # 指标类实例
        self.index_18 = WiMA_index.wilder_MA(input_contract.symbol+'_'+input_contract.currency, 18)
        self.index_25 = WiMA_index.wilder_MA(input_contract.symbol+'_'+input_contract.currency, 25)


    def get_current_state(self, current_state: int):
        self.current_state = current_state


    def skip_first_N_cycles(self):
        # 跳过前10个周期
        if self.current_cycles < self.cancel_first_N_cycles:
            self.current_cycles += 1
        else:
            self.cycles_ok = 1
        # print("working")


    def get_price(self, price: float):
        # 从tickPrice函数中获得最新的标的价格，更新实例变量price。
        self.price = price

        # 该函数负责根据最新标的物价格更新技术指标。
        self.index_18.update_current_index(price)
        self.index_25.update_current_index(price)
        self.price_1 = self.index_18.wiMA_30min
        self.price_2 = self.index_25.wiMA_30min

        # print(self.price_1, self.price_2, "abc")


    def judgement(self):
        # 判断标的实时价格与双均线位置关系，1代表双均线之上，-1代表双均线之下，0代表双均线之间
        if self.price > max(self.price_1, self.price_2):
            return_value = 1
        elif self.price < min(self.price_1, self.price_2):
            return_value = -1
        else:
            return_value = 0

        return return_value


    def strategy_exe(self):
        # 策略函数，根据现阶段价格位置和现阶段多空仓位情况，判断下单方向。
        # action = 1 代表下达买单
        # action = -1 代表下达卖单
        # action = 0 代表不动作

        position = self.judgement()


        # 执行策略1
        action = self.strategy_2(position)



        if action == 1:
            return_tuple = (self.contract, limitOrder("BUY", self.quantity, round(self.price, 2)))
            # return_tuple = (self.contract, marketOrder("BUY", self.quantity))
            print("buy", self.quantity, "@", "price", round(self.price, 2), "\t\t\tindex_18:", self.price_1,
                  "\t\t\tindex_25:", self.price_2)

        elif action == -1:
            return_tuple = (self.contract, limitOrder("SELL", self.quantity, round(self.price, 2)))
            # return_tuple = (self.contract, marketOrder("SELL", self.quantity))
            print("sell", self.quantity, "@", "price", round(self.price,2), "\t\t\tindex_18:", self.price_1,
                  "\t\t\tindex_25:", self.price_2)

        elif action == 0:
            return_tuple = ("hold", "hold")
        else:
            return_tuple = ("hold", "hold")
            print("place order error!!!!")

        if self.cycles_ok == 0:
            return_tuple = ("hold", "hold")

        return return_tuple



        # 测试代码
        # if action == 1:
        #     print("buy", self.quantity, "@", "price", self.price)
        #     print("state:", self.long_or_short)
        # elif action == -1:
        #     print("sell", self.quantity, "@", "price:", self.price)
        #     print("state:", self.long_or_short)
        # elif action == 0:
        #     pass
        #     # print("do nothing")
        # else:
        #     print("place order error!!!!")
        #
        # return ("hold","hold")


    def strategy_1(self, position):
        # 当价格高于双均线时开多仓，当价格低于双均线时开空仓，在双均线之间时平仓
        action = 0
        if self.current_state == 0:
            action = position
        elif self.current_state == 1:
            if position == 1:
                action = 0
            else:
                action = -1
        elif self.current_state == -1:
            if position == -1:
                action = 0
            else:
                action = 1
        # 测试用
        # print("current_state: ", self.current_state)
        return action

    def strategy_2(self, position):
        # 当价格高于双均线时开多仓，当价格低于双均线时开空仓，在双均线之间时无动作
        action = 0
        if self.current_state == 0:
            action = position
        elif self.current_state == 1:
            if position == -1:
                action = -1
            else:
                action = 0
        elif self.current_state == -1:
            if position == 1:
                action = 1
            else:
                action = 0
        return action
