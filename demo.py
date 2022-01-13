from BadBehavior.BadBehavior import BadBehavior
from BadBehavior.operation import *
from read_data import read_data
from visualization import plot_heat_map

path_gps = r"/Users/zengxingchen/Desktop/大三/交科赛/gps_20161102.csv"

if __name__ == '__main__':
    traces = read_data(path_gps, major_id="id1", sub_id="id2")
    bad_behavior = BadBehavior(traces)

    op1 = RapidAccelerateOP()
    bad_behavior.set_op(op1)
    bad_behavior.compute()
    bad_behavior.time_hist()

    # op2 = RapidAccelerateOP()
    # bad_behavior.set_op(op2)
    # bad_behavior.compute()
    # bad_behavior.time_hist()

    # 热图
    heatmap = plot_heat_map(bad_behavior.get_pos())
    heatmap.save('./heatmap_rapid_accelerate.html')
