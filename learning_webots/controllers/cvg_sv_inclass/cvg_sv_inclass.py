from controller import Supervisor
import numpy as np
from matplotlib import pyplot as plt

supervisor = Supervisor()
step = int(supervisor.getBasicTimeStep())

WhW = 0.5 # the world is a square

RID = 0
def add_epuck():
    global RID
    pos = np.random.uniform(-WhW, WhW, size=2)
    epuck_string = f'''
        DEF EPUCK{RID} E-puck {{
        name "EPUCK{RID}"
        translation {pos[0]} {pos[1]} 0.01
        rotation 0 0 1 {np.random.uniform(0, 2 * np.pi)}
        controller "RW4"
    }}
    '''
    supervisor.getRoot().getField("children").importMFNodeFromString(-1, epuck_string)
    RID += 1

NR =  10

for i in range(NR):
    add_epuck()

robots = []
for i in range(NR):
    robots.append(supervisor.getFromDef(f"EPUCK{i}"))

robot_pos_history = []
last_plot = 0

while supervisor.step(step) != -1:

    for i in range(NR):
        pos = robots[i].getPosition()[:2]
        robot_pos_history.append(pos)

    if supervisor.getTime() - last_plot > 200:
        # plot the pos
        plt.scatter(np.array(robot_pos_history)[:,0], np.array(robot_pos_history)[:,1], s=1)
        plt.xlim(-WhW, WhW)
        plt.ylim(-WhW, WhW)
        print(np.shape(robot_pos_history))
        plt.show()
        last_plot = supervisor.getTime()
        # pause the simulation
        supervisor.simulationSetMode(Supervisor.SIMULATION_MODE_PAUSE)

