from math import atan2, degrees
import pandas as pd
import numpy as np

def px2deg(screen_size, distance, screen_resolution):
    """
    px2deg converts pixels of coordinates to degrees.
    It helps eye movement classifiers work based on degrees.
    Because the velocity is likely used in visual degrees per second, it is beneficial to calculate the pixel to degrees.
    
    If you want to find more information about the advantages of utilizing degrees
    , when it comes to the task, please refer [1] and [2]
    
    # Attributes
    screen_size(width, cm) = The screen_size excluding bezel used in your environment.
    distance(cm) = The distance between your eyes and your monitor. Normally, it is around 70
    screen_resolution(width, px) = The width resolution of your monitor.
    
    ex) px2deg(60, 70, 1920)
    """
    return degrees(atan2(0.5 * screen_size, distance)) / (0.5 * screen_resolution)

def gap_fill_in(data):
    data = pd.read_csv(data)
    ts, x, y = np.array(data['ts']), np.array(data['x']), np.array(data['y'])
    max_gap_length = 75
    
    nan_index = np.argwhere(np.isnan(x))
    gaps = []
    gap = False
    temp_gap = []
    
    for i in nan_index:
        if (i+1) in nan_index:
            gap = True
            temp_gap.append(i)
        elif ((i+1) not in nan_index) and (gap == True):
            gap = False
            temp_gap.append(i)
            gaps.append(temp_gap)
            temp_gap = []
        elif ((i+1) not in nan_index) and (gap == False):
            gaps.append(i)
    
    for gap in gaps:
        if (ts[np.max(gap)] - ts[np.min(gap)-1]) < max_gap_length:
            cor_data_x =[
                [ts[np.max(gap)+1], x[np.max(gap)+1]],
                [ts[np.min(gap)-1], x[np.min(gap)-1]],
            ]
            cor_data_y = [
                [ts[np.max(gap)+1], y[np.max(gap)+1]],
                [ts[np.min(gap)-1], y[np.min(gap)-1]],
            ]
            for index in gap:
                x[index] = linear_interpolation(cor_data_x, ts[index])
                y[index] = linear_interpolation(cor_data_y, ts[index])
                
    return x, y, ts

def linear_interpolation(data, target_x):
    """
    data = list([data_x_1, data_y_1], [data_x_2, data_y_2])
    target_x = x from missing value
    """
    target_y = ((data[1][0] - data[0][0]) \
                / (data[1][1] - data[0][1])) \
                * (target_x - data[1][0]) + data[1][1]
    
    return target_y