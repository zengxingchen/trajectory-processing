import pandas as pd
from Trace import Trace
from BadBehavior.config import split_trace_threshold, path_gps
from visualization import plot_map


# major_id决定是一个司机id对应一条轨迹还是一个order_id对应一条轨迹
def read_data(path_gps, nrows=100000, major_id="id2", sub_id="id1"):
    # TODO 这个函数太大了，拆成两个
    data_small = pd.read_csv(path_gps, names=["id1", "id2", "time", "lon", "lat"], nrows=nrows)  # 先用前10万数据测试
    # 获取所有订单id（即轨迹id）
    trace_ids = data_small[major_id].unique()
    # 求出所有轨迹
    traces_ = []
    for t in trace_ids:
        trace_df = data_small.loc[data_small[major_id] == t, :]
        if major_id == "id1":
            # 如果是以司机id划分轨迹，首先求出该司机的所有order_id对应的轨迹
            order_traces = []
            order_ids = trace_df["id2"].unique()
            for order_id in order_ids:
                order_trace = Trace(order_id, t)
                order_df = trace_df[trace_df["id2"] == order_id]
                for _, line in order_df.iterrows():
                    order_trace.add((line['lon'], line['lat']), line['time'])
                order_traces.append(order_trace)

            # 对订单轨迹按首个轨迹点时间排序，之后合成为司机轨迹，轨迹间时间间隔过长的轨迹不合并，另开轨迹
            order_traces.sort(key=lambda x: x.times[0])
            trace = []  # 这时候的trace的id就不重要了
            for order_trace in order_traces:
                if len(trace) == 0 or order_trace.times[0] - trace[-1].times[-1] > split_trace_threshold:
                    trace.append(order_trace)
                else:
                    trace[-1].times.extend(order_trace.times)
                    trace[-1].points.extend(order_trace.points)
        # 单纯的一个订单对应一条轨迹
        else:
            assert trace_df[sub_id].unique().shape[0] == 1
            trace = Trace(t, trace_df[sub_id].iloc[0])
            for _, line in trace_df.iterrows():
                trace.add((line['lon'], line['lat']), line['time'])
        if isinstance(trace, list):
            traces_.extend(trace)
        else:
            traces_.append(trace)
    return traces_


if __name__ == '__main__':
    traces = read_data(path_gps, major_id="id1", sub_id="id2")
    # 把第一条轨迹绘制到地图上
    trace = traces[0]
    map = plot_map(trace)#调用visualization里的接口
    print('正在绘制地图')
    map.save('./map.html')
    print('绘制完毕，地图生成为map.html')

    
