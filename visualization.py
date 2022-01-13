import folium
from folium.plugins import HeatMap
import matplotlib.pyplot as plt


# 将一条轨迹绘制到地图上
def plot_map(trace):
    temp_map = folium.Map(location=[sum(trace.latitude) / len(trace.latitude),
                                    sum(trace.longitude) / len(trace.longitude)],
                          zoom_start=18,
                          attr='http://ditu.amap.com/')
    folium.PolyLine(list(zip(trace.latitude, trace.longitude)),
                    weight=3,
                    opacity=0.8,
                    color='orange').add_to(temp_map)
    for point_index, point in enumerate(trace.points):
        temp_map.add_child(
            folium.Marker(
                list(reversed(point)), tooltip=trace.info(point_index)
            )
        )
    return temp_map


# 默认接受的值是二维坐标数组(ndarray类型)
def plot_heat_map(points):
    temp_map = folium.Map(location=[points[:, 1].mean(), points[:, 0].mean()],
                          zoom_start=12)
    # (经度,纬度)转换成(纬度,经度)
    heatdata = points[:, [1, 0]]
    HeatMap(heatdata).add_to(temp_map)
    return temp_map
