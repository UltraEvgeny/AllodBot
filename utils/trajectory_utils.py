from utils.funcs import yaml_load
import numpy as np


def load_trajectory(trajectory_name):
    points = yaml_load(f'trajectories/{trajectory_name}.yaml')
    for point in points:
        point['coords'] = np.array(point['coords'])
    return points


def forward_backward_generator(arr, initial_i):
    cur_direction = 1
    cur_i = initial_i
    while True:
        print(cur_i, arr[cur_i])
        yield arr[cur_i]
        if cur_direction == 1 and cur_i == len(arr) - 1 or cur_direction == -1 and cur_i == 0:
            cur_direction *= -1
        cur_i += cur_direction


def get_nearest_point_i(single_point, points):
    r = ((points - single_point)**2).sum(axis=1).argmin()
    return r
