from math import atan2, degrees
import pandas as pd
import numpy as np

def px2deg(screen_size, distance, screen_resolution):
    """
    screen_size(width) = cm
    distance = cm
    screen_resolution(width) = px
    ex) px2deg(60, 70, 1920)
    """
    return degrees(atan2(0.5 * screen_size, distance)) / (0.5 * screen_resolution)

def gap_fill_in(data, max_gap_length = 75):
    """
    data = "file_name.csv"
    max_gap_length = ms
    sacling_factor = (t_timestamp of sample to be replaced - t_timestamp of first sample after gap) / \
        (t_timestamp of last sample before gap - t_timestamp of first sample after gap)

    This function should not be used when the data has a low sampling rate, or the accuracy of analyses is anticipated as high.
    ex) gap_fill_in("input.csv")
    """
    # Read the csv file.
    df = pd.read_csv(data)

    # 
    