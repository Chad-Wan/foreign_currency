from wrapper_class import app_client
from investment import *


# 账户名称
account = "DU859178"
my_contract = EUR_JPY()

my_client = app_client(my_contract, account)

# 启动 client 与 TWS之间的链接
my_client.connect("127.0.0.1", 7496, clientId=0)

# 开始获取市场数据，启动数据流
my_client.reqMktData(110, my_contract, "221", False, False, [])

# 取消所有订单
my_client.reqGlobalCancel()

# 获取持仓信息
my_client.reqPositions()

# my_client.reqMktData(111, my_contract, "225", False, False, [])

# my_client.placeOrder(300, my_contract, limitOrder("BUY", 20000, 0.9))   # 下单

my_client.run()

