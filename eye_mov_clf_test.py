from math import atan2, degrees
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

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

def load_data(file_name):
    data = pd.read_csv(file_name)
    ts, x, y = np.array(data['ts']), np.array(data['x']), np.array(data['y'])

    return ts, x, y


def gap_fill_in(ts, x, y):
    """
    ts(ms) = timestamp
    x(px) = x coordinate
    y(px) = y coordinate
    max_gap_length(ms) = the duration between a last valid point before the gap and a last point in the gap

    """
    ts, x, y = ts, x, y
    
    max_gap_length = 75
    
    nan_index = np.argwhere(np.isnan(x))
    gap = False
    gaps = []
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
                
    return ts, x, y

def linear_interpolation(data, target_x):
    """
    The gap is filled by utilizing linear_interpolation function.
    This is the basic way to interpolate missing data.

    data = list([data_x_1, data_y_1], [data_x_2, data_y_2])
    target_x = x from missing value
    """
    target_y = ((data[1][0] - data[0][0]) \
                / (data[1][1] - data[0][1])) \
                * (target_x - data[1][0]) + data[1][1]
    
    return target_y

def noise_reducing(nums, window, method = 'med'):
    
    """
    This function reduces noises of data using median or average method.
    Default is median for following a guideline of Tobii.
    """
    reduced_nums = np.array([])
    if method == 'avg':
        for i in range(len(nums)):
            if np.isnan(nums[i]):
                reduced_nums = np.append(reduced_nums, nums[i])
            elif i < window:
                for j in reversed(range(i+1)):
                    if j != 0:
                        reduced_nums = np.append(reduced_nums, np.nanmean(nums[i-j:i+j]))
                        break
                    else:
                        reduced_nums = np.append(reduced_nums, nums[i])
            elif i >= (len(nums) - window):
                for j in reversed(range(len(nums) - i)):
                    if j != 0:
                        reduced_nums = np.append(reduced_nums, np.nanmean(nums[i-j:i+j]))
                        break
                    else:
                        reduced_nums = np.append(reduced_nums, nums[i])
            else:
                reduced_nums = np.append(reduced_nums, np.nanmean(nums[i-window:i+window]))
    elif method == 'med':
        for i in range(len(nums)):
            if np.isnan(nums[i]):
                reduced_nums = np.append(reduced_nums, nums[i])
            elif i < window:
                for j in reversed(range(i+1)):
                    if j != 0:
                        reduced_nums = np.append(reduced_nums, np.nanmedian(nums[i-j:i+j]))
                        break
                    else:
                        reduced_nums = np.append(reduced_nums, nums[i])
            elif i >= (len(nums) - window):
                for j in reversed(range(len(nums) - i)):
                    if j != 0:
                        reduced_nums = np.append(reduced_nums, np.nanmedian(nums[i-j:i+j]))
                        break
                    else:
                        reduced_nums = np.append(reduced_nums, nums[i])
            else:
                reduced_nums = np.append(reduced_nums, np.nanmedian(nums[i-window:i+window]))
    return reduced_nums

def drawing_seperate_scatter(coordinate_data):
    """
    coordinate_data = dict('X coordinate': x, 'Y coordinate': y, 'Timestamp': ts)
    """
    legend = ['X coordinate', 'Y coordinate']
    plt.scatter(coordinate_data['Timestamp'], coordinate_data['X coordinate'])
    plt.scatter(coordinate_data['Timestamp'], coordinate_data['Y coordinate'])
    plt.xlabel('Timestamp')
    plt.ylabel('Coordinate')
    plt.legend(legend)
    return plt.show()

def drawing_xy_scatter(coordinate_data):
    """
    coordinate_data
    """
    plt.scatter(coordinate_data['X coordinate'], coordinate_data['Y coordinate'], color = 'skyblue')
    plt.xlabel('X coordinate')
    plt.ylabel('Y coordinate')
    return plt.show() 