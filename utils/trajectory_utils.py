from utils.funcs import yaml_load
import numpy as np


def load_trajectory(trajectory_name):
    points = yaml_load(f'trajectories/{trajectory_name}.yaml')
    for point in points:
        point['coords'] = np.array(point['coords'])
    return points

