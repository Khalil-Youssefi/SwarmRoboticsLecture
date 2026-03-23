import numpy as np
def fitness(pos_x, pos_y, TARGET_X=5, TARGET_Y=5):
    # rastrigin function
    rastrigin = 10 * 2 + (pos_x - TARGET_X) ** 2 - 10 * np.cos(2 * np.pi * (pos_x - TARGET_X)) + (pos_y - TARGET_Y) ** 2 - 10 * np.cos(2 * np.pi * (pos_y - TARGET_Y))
    return rastrigin