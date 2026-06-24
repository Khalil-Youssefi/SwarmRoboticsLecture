from controller import Supervisor
import numpy as np
supervisor = Supervisor()
step = int(supervisor.getBasicTimeStep())

# add E-puck by string
epuck_string = "DEF EPUCK1 E-puck { name \"EPUCK1\" translation -0.1 0.1 0.01 rotation 0 0 1 1.14 controller \"in_class_light_follow\" }"

def add_epuck(id,pos,yaw):
    epuck_string = f'''
        DEF EPUCK{id} E-puck {{
        name "EPUCK{id}"
        translation {pos[0]} {pos[1]} 0.01
        rotation 0 0 1 {yaw}
        controller "in_class_light_follow"
    }}
    '''
    supervisor.getRoot().getField("children").importMFNodeFromString(-1, epuck_string)
# directly add the E-puck to the scene

THmin, THmax = -0.35, 0.35
poses = []
for i in range(5):
    pos = np.random.uniform(THmin, THmax, size=2)
    for other_pos in poses:
        while np.linalg.norm(pos - other_pos) < 0.07:
            pos = np.random.uniform(THmin, THmax, size=2)
    yaw = np.random.uniform(0, 2 * np.pi)
    add_epuck(i, pos, yaw)
    poses.append(pos)

def add_obstacle(id, pos):
    obstacle_string = f'''
        DEF OBSTACLE{id} obstacle_inclass {{
        translation {pos[0]} {pos[1]} 0.035
        }}
    '''
    supervisor.getRoot().getField("children").importMFNodeFromString(-1, obstacle_string)

for i in range(15):
    pos = np.random.uniform(THmin, THmax, size=2)
    for other_pos in poses:
        while np.linalg.norm(pos - other_pos) < 0.15:
            pos = np.random.uniform(THmin, THmax, size=2)
    add_obstacle(i, pos)
    poses.append(pos)