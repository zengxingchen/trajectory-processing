import numpy as np
from pygeodesy.sphericalNvector import LatLon
from numpy import sin
from numpy import cos
from numpy import arctan
import time

# 将轨迹封装成类
class Trace:
    def __init__(self, trace_id, driver_id):
        # 公有属性
        self.id = trace_id
        self.driver_id = driver_id
        self.times = []
        self.points = []
        self.longitude = []
        self.latitude = []
        self.num = 0
        # 私有属性
        self._velocity = []
        self._acceleration = []
        self._turn_angle = []
        self._turn_angle_change_rate = []

    def add(self, point, point_time):
        self.points.append(point)
        self.longitude.append(point[0])
        self.latitude.append(point[1])
        self.times.append(point_time)
        self.num += 1

    def __len__(self):
        return len(self.points)

    # 一条轨迹的总时间
    @property
    def total_time(self):
        if len(self.times) <= 0:
            raise ValueError("Please add times to trace firstly!")
        return self.times[-1] - self.times[0]

    # 速度
    @property
    def v(self):
        if len(self.points) <= 0 or len(self.times) <= 0:
            raise ValueError("Please add points and times to trace!")

        if len(self._velocity) > 0:
            return self._velocity
        else:
            self._velocity.append(np.nan)  # 第一个点的速度未知
            for i in range(1, len(self.times) - 1):
                start_time = self.times[i - 1]
                end_time = self.times[i + 1]
                start_position = self.points[i - 1]
                end_position = self.points[i + 1]

                # 使用pygeodesy库的LatLon求距离
                start = LatLon(start_position[1], start_position[0])  # LatLon坐标顺序是(纬度，经度)
                end = LatLon(end_position[1], end_position[0])

                distance = start.distanceTo(end)
                cost_time = end_time - start_time

                self._velocity.append(distance / cost_time)
            self._velocity.append(np.nan)  # 最后一个点的速度未知
            return self._velocity

    # 加速度
    @property
    def a(self):
        if len(self.points) <= 0 or len(self.times) <= 0:
            raise ValueError("Please add points and times to trace!")

        if len(self._velocity) <= 0:
            raise ValueError("Please initialize _velocity before initializing _acceleration!")
        if len(self._acceleration) > 0:
            return self._acceleration
        else:
            # 前两个点的加速度未知
            self._acceleration.append(np.nan)
            self._acceleration.append(np.nan)
            for i in range(2, len(self._velocity) - 2):
                start_time = self.times[i - 1]
                end_time = self.times[i + 1]
                start_v = self._velocity[i - 1]
                end_v = self._velocity[i + 1]

                delta_v = end_v - start_v
                cost_time = end_time - start_time

                self._acceleration.append(delta_v / cost_time)
            # 最后两个点的加速度未知
            self._acceleration.append(np.nan)
            self._acceleration.append(np.nan)
            return self._acceleration

    # 转向角
    @property
    def angle(self):
        if len(self.points) <= 0 or len(self.times) <= 0:
            raise ValueError("Please add points and times to trace!")
        if len(self._turn_angle) > 0:
            return self._turn_angle
        else:
            for i in range(len(self.times) - 1):
                start_position = self.points[i]
                end_position = self.points[i + 1]

                y = sin(end_position[0] - start_position[0]) * cos(end_position[1])
                x = cos(start_position[1]) * sin(end_position[1]) - sin(start_position[1]) * cos(end_position[1]) * \
                    cos(end_position[0] - start_position[0])
                if x == 0:
                    Bi = np.pi
                else:
                    Bi = arctan(y / x)
                self._turn_angle.append(Bi)
            # 最后一个点的转向角未知
            self._turn_angle.append(np.nan)
            return self._turn_angle

    # 转向角变化率
    @property
    def angle_change_rate(self):
        if len(self._turn_angle) <= 0:
            raise ValueError("Please initialize turn angle before initializing angle change rate!")
        if len(self._turn_angle_change_rate) > 0:
            return self._turn_angle_change_rate
        else:
            for i in range(len(self._turn_angle) - 2):
                start_time = self.times[i]
                end_time = self.times[i + 1]
                start_angle = self._turn_angle[i]
                end_angle = self._turn_angle[i + 1]

                delta_angle = end_angle - start_angle
                cost_time = end_time - start_time

                self._turn_angle_change_rate.append(delta_angle / cost_time)

            self._turn_angle_change_rate.append(np.nan)
            self._turn_angle_change_rate.append(np.nan)

            return self._turn_angle_change_rate

    # 将时间转化为年月日 时分秒的形式
    @classmethod
    def get_real_time(cls, time_from_1970):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_from_1970))

    def info(self, point_index):
        return f"时间: {self.get_real_time(self.times[point_index])}<br>" \
               f"速度: {self.v[point_index]}<br>" \
               f"加速度: {self.a[point_index]}<br>" \
               f"转向角: {self.angle[point_index]}<br>" \
               f"转向角变化率: {self.angle_change_rate[point_index]}"