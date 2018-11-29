import datetime


class wilder_MA():
    # 调用方法：test
    # instance1 = wilder_MA(USD_JPY, 15) 15怀尔德均线；instance1.wiMA_30min 为30分钟15怀尔德均线
    # instance2 = wilder_MA(USD_JPY, 20) 15怀尔德均线；instance2.wiMA_1day 为天线的15怀尔德均线
    def __init__(self, investment: str, period: int):
        # 指标参数
        self.period = period

        # 当前技术指标
        self.wiMA_10min = 0.0
        self.wiMA_30min = 0.0
        self.wiMA_1hour = 0.0
        self.wiMA_1day = 0.0

        # 上一周期技术指标
        self.wiMA_10min_old = 0.0
        self.wiMA_30min_old = 0.0
        self.wiMA_1hour_old = 0.0
        self.wiMA_1day_old = 0.0

        now = datetime.datetime.now()
        self.last_overwrite_time_10min = now
        self.last_overwrite_time_30min = now
        self.last_overwrite_time_1hour = now
        self.last_overwrite_time_1day = now

        # 从文件中读取上一周期的均线指标，存入*_old数据中
        history_index_path = "I:\\forex_database\\Wilder_MA_db" + str(period)
        f = open(history_index_path, 'r')
        lines = f.readlines()
        f.close()

        for line in lines:
            investment_inFile, index, data = line.split()
            if investment_inFile == investment and index == "wiMA_10min":
                self.wiMA_10min_old = float(data)
            elif investment_inFile == investment and index == "wiMA_30min":
                self.wiMA_30min_old = float(data)
            elif investment_inFile == investment and index == "wiMA_1h":
                self.wiMA_1hour_old = float(data)
                # 测试指标用
                # print("10min avg:",self.wiMA_10min_old,"30min avg:",self.wiMA_30min_old,"1h avg:",
                #       self.wiMA_1h_old, "1day avg:",self.wiMA_1day_old , "investment", investment)
            elif investment_inFile == investment and index == "wiMA_1d":
                self.wiMA_1day_old = float(data)

    def update_current_index(self, price: float):
        # 更新当前技术指标
        self.wiMA_10min = price / self.period + self.wiMA_10min_old * (self.period - 1) / self.period
        self.wiMA_30min = price / self.period + self.wiMA_30min_old * (self.period - 1) / self.period
        self.wiMA_1hour = price / self.period + self.wiMA_1hour_old * (self.period - 1) / self.period
        self.wiMA_1day = price / self.period + self.wiMA_1day_old * (self.period - 1) / self.period

        # print(self.wiMA_30min, self.wiMA_30min_old, price, self.period)

    def update_last_wiMA(self):
        # 判断是否已经进入下一周期，如果是的话更新*_old变量
        now = datetime.datetime.now()
        if now - self.last_overwrite_time_10min > datetime.timedelta(minutes=10):
            self.wiMA_10min_old = self.wiMA_10min
            self.last_overwrite_time_10min = now
            # 测试代码： 每十分钟回报一次指标参数
            print(now, "\t10m:", self.wiMA_10min, "\t30m:", self.wiMA_30min, "\t1h:", self.wiMA_1hour, "\t1d:", self.wiMA_1day)

        if now - self.last_overwrite_time_30min > datetime.timedelta(minutes=30):
            self.wiMA_30min_old = self.wiMA_30min
            self.last_overwrite_time_30min = now

        if now - self.last_overwrite_time_1hour > datetime.timedelta(hours=1):
            self.wiMA_1hour_old = self.wiMA_1hour
            self.last_overwrite_time_1hour = now

        if now - self.last_overwrite_time_1day > datetime.timedelta(days=1):
            self.wiMA_1day_old = self.wiMA_1day
            self.last_overwrite_time_1day = now























