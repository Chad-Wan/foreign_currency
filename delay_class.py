import datetime

class delay_class():
    def __init__(self):
        now = datetime.datetime.now()
        pass

    def delay_sec(self, num: int):
        now = datetime.datetime.now()
        count = now.second % num
        pass

    def delay_min(self, num: int):
        now = datetime.datetime.now()
        count = now.minute % num
        pass

    def delay_hour(self, num: int):
        now = datetime.datetime.now()
        count = now.hour % num
        pass

    def delay_day(self, num: int):
        now = datetime.datetime.now()
        count = now.day % num
        pass

    def if_in_range(self, count: int, num: int):
        # delay 的时间必须是能整除60的数
        if count < num // 2 and not self.last_value_0:
            self.delay_done = True
            self.last_value_0 = True
        elif count < num // 2 and self.last_value_0:
            self.delay_done = False
            # print("delaying", count, self.last_value_0)
        else:
            self.last_value_0 = False