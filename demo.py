from BadBehavior.BadBehavior import BadBehavior
from BadBehavior.operation import *
from BadBehavior.config import path_gps
from read_data import read_data
from visualization import plot_heat_map


if __name__ == '__main__':
    traces = read_data(path_gps, major_id="id1", sub_id="id2")
    bad_behavior = BadBehavior(traces)
    # 批处理所有的异常行为
    op_list = [OverSpeedOP(), FatigueDrivingOP(), RapidAccelerateOP(), 
                StabilityOP(), SharpTurnOP()]
    # 如需测试单个异常行为，修改op_list即可
    #op_list = [RapidAccelerateOP()]
    
    for op in op_list:
        bad_behavior.set_op(op)
        bad_behavior.compute()
        # 直方图
        bad_behavior.time_hist()
        # 热图
        heatmap = plot_heat_map(bad_behavior.get_pos())
        heatmap.save('./results/heatmap_' + op.kind +'.html')
