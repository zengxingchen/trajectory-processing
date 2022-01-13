from BadBehavior.config import *
from Trace import Trace
from numpy import std


class BadBehaviorPoint:
    """
    记录一次不良行为，包含属性：
    不良行为类型
    不良行为的发生经度、纬度
    不良行为的发生时间
    不良行为的司机id
    不良行为的订单id
    """
    def __init__(self, kind, lon, lat, time, driver_id, order_id):
        self.kind = kind
        self.lon = lon
        self.lat = lat
        self.time = time
        self.driver_id = driver_id
        self.order_id = order_id


class BadBehaviorOP:
    """
    抽象类，用于计算不良行为
    """
    def __init__(self, kind=None):
        self.kind = kind

    def compute(self, trace):
        """
        这个函数根据传入的一条轨迹，计算轨迹内的相应的不良行为点，返回点的列表
        """
        raise NotImplementedError


class OverSpeedOP(BadBehaviorOP):
    """
    超速
    """
    def __init__(self):
        super().__init__("OverSpeed")

    def compute(self, trace):
        res = []
        length = len(trace)
        for idx in range(1, length - 1):
            if trace.v[idx] > overspeed_threshold:
                res.append(BadBehaviorPoint(self.kind,
                                            trace.points[idx][0],
                                            trace.points[idx][1],
                                            trace.times[idx],
                                            trace.driver_id,
                                            trace.id))
        return res


class FatigueDrivingOP(BadBehaviorOP):
    """
    疲劳驾驶
    """
    def __init__(self):
        super().__init__("FatigueDriving")

    def get_day_night(self, time_1970):
        time_str = Trace.get_real_time(time_1970)
        time_hour = int(time_str.split(" ")[1].split(":")[0])
        if fatigue_driving_day_threshold <= time_hour < fatigue_driving_night_threshold:
            return "day"
        else:
            return "night"

    def compute(self, trace):
        res = []
        # 记录疲劳驾驶的点，一旦超过阈值，除非休息时间超过阈值，不然后面点都算疲劳驾驶
        start = trace.times[0]
        end = start
        index = 0
        while index < len(trace):
            if trace.v[index] == 0:
                zero_start = trace.times[index]
                # 前进至一个速度不为0的点
                index += 1
                while index < len(trace) and trace.v[index] == 0:
                    index += 1
                if index == len(trace):
                    break
                zero_end = trace.times[index]

                if zero_end - zero_start > fatigue_driving_rest_threshold:
                    start = zero_end
            end = trace.times[index]

            if self.get_day_night(end) == "day" and end - start > fatigue_driving_day_threshold or \
               self.get_day_night(end) == "night" and end - start > fatigue_driving_night_threshold:
                res.append(BadBehaviorPoint(self.kind,
                                            trace.points[index][0],
                                            trace.points[index][1],
                                            trace.times[index],
                                            trace.driver_id,
                                            trace.id))
            index += 1
        return res


class RapidAccelerateOP(BadBehaviorOP):
    """
    急加减速
    """
    def __init__(self):
        super().__init__("RapidAccelerate")

    def compute(self, trace):
        res = []
        length = len(trace)
        for idx in range(2, length - 2):
            speed = trace.v[idx]
            rank = None
            for i in range(len(speed_section) - 1):
                if speed_section[i] <= speed < speed_section[i + 1]:
                    rank = i
                    break
            assert rank is not None
            acc = trace.a[idx]
            if acc > 0 and acc > rapid_accelerate_threshold[rank] or acc < 0 and acc < rapid_slowdown_threshold[rank]:
                res.append(BadBehaviorPoint(self.kind,
                                            trace.points[idx][0],
                                            trace.points[idx][1],
                                            trace.times[idx],
                                            trace.driver_id,
                                            trace.id))
        return res


class StabilityOP(BadBehaviorOP):
    """
    稳定性
    使用滑动窗口，若一个窗口内的点的速度的方差大于阈值，则将窗口的开始点加入到异常行为点集中
    TODO 这种方法实在太糙，以后改进一下
    """
    def __init__(self):
        super().__init__("Stability")

    def compute(self, trace):
        res = []
        for idx in range(len(trace) - window_size):
            v_window = trace.v[idx: idx + window_size]
            if std(v_window) > variance_threshold:
                res.append(BadBehaviorPoint(self.kind,
                                            trace.points[idx][0],
                                            trace.points[idx][1],
                                            trace.times[idx],
                                            trace.driver_id,
                                            trace.id))
        return res


class SharpTurnOP(BadBehaviorOP):
    """
    急转弯
    """
    def __init__(self):
        super().__init__("SharpTurn")

    def compute(self, trace):
        res = []
        length = len(trace)
        for idx in range(length - 1):
            if trace.angle[idx] > turn_angle_threshold:
                res.append(BadBehaviorPoint(self.kind,
                                            trace.points[idx][0],
                                            trace.points[idx][1],
                                            trace.times[idx],
                                            trace.driver_id,
                                            trace.id))
        return res
