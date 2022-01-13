from numpy import pi
"""
这个文件最好由交院的同学完成
"""

# 默认单位是m/s、m/s^2、s、小时

# 超速阈值
overspeed_threshold = 33.0

# 四个速度区间
speed_section = [0, 30.0, 40.0, 60.0, 10000000]

# 四个速度区间的危险加减速度阈值
rapid_accelerate_threshold = [2.5, 2.2, 2.1, 1.95]
rapid_slowdown_threshold = [-2.25, -1.95, -1.85, -1.7]

# 四个速度区间的角速度阈值
angle_speed_threshold = [7.5, 6, 6, 5]

# 划分白天黑夜的点，两个点之间算是白天
day_start = 8
day_over = 18

# 切分轨迹的时间阈值
split_trace_threshold = 1800

# 疲劳驾驶的两个阶段的阈值
# 白天的驾驶时长阈值
fatigue_driving_day_threshold = 14400
# 晚上的驾驶时长阈值
fatigue_driving_night_threshold = 7200

# 疲劳驾驶休息时间阈值
fatigue_driving_rest_threshold = 1800

# 转向角的阈值
turn_angle_threshold = pi / 3

# 计算稳定性的窗口大小
window_size = 5
# 判定稳定性的方差阈值
variance_threshold = 20.0
