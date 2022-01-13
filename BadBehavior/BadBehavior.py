from BadBehavior.operation import BadBehaviorOP
import numpy as np
from Trace import Trace
import matplotlib.pyplot as plt
import pandas as pd
# 本地字体配置，自行注释掉
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

class BadBehavior:
    def __init__(self, traces):
        self.traces = traces
        self.points = []
        self.op = BadBehaviorOP()
        self.op_name = ''

    def set_op(self, op):
        self.points = []
        self.op = op

    # 计算出所有的不良行为点
    def compute(self):
        print(f"计算不良驾驶行为 {self.op.kind}")
        for trace in self.traces:
            self.points.extend(self.op.compute(trace))

    # 绘制不良驾驶行为的时间频率直方图
    def time_hist(self):
        times = []
        for point in self.points:
            time_str = Trace.get_real_time(point.time)
            # 原时间格式是 %Y-%m-%d %H:%M:%S，得到时
            hour = time_str.split(" ")[1].split(":")[0]
            times.append(int(hour))
        plt.hist(times, bins=24)
        plt.ylabel(self.op_name + "的发生频次（次）")
        plt.xlabel(self.op_name + "的发生时段（时）")
        plt.savefig('./results/' + self.op.kind + '_hist'+ ".png") # 方便批处理所有异常行为
        # plt.show()

    # 统计司机的不良行为数
    def driver_analysis(self):
        drivers = [p.driver_id for p in self.points]
        res = pd.value_counts(drivers)
        # res.to_csv(f"./{self.op.kind}_driver.csv")  # 导出为csv
        return res

    # 聚类/可视化要用，导出相应不良驾驶行为所有点的坐标
    def get_pos(self):
        pos = []
        for point in self.points:
            pos.append([point.lon, point.lat])
        return np.array(pos)
