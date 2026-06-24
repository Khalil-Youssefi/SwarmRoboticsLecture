from controller import Supervisor
from matplotlib import pyplot as plt
import numpy as np
supervisor = Supervisor()
step = int(supervisor.getBasicTimeStep())

def add_epuck(id,pos,yaw):
    epuck_string = f'''
        DEF EPUCK{id} E-puck {{
        name "EPUCK{id}"
        translation {pos[0]} {pos[1]} 0.01
        rotation 0 0 1 {yaw}
        controller "swarm_random_walk"
    }}
    '''
    supervisor.getRoot().getField("children").importMFNodeFromString(-1, epuck_string)
# directly add the E-puck to the scene

THmin, THmax = -0.45, 0.45
poses = []
for i in range(5):
    pos = np.random.uniform(THmin, THmax, size=2)
    for other_pos in poses:
        while np.linalg.norm(pos - other_pos) < 0.07:
            pos = np.random.uniform(THmin, THmax, size=2)
    yaw = np.random.uniform(0, 2 * np.pi)
    add_epuck(i, pos, yaw)
    poses.append(pos)

robot_pos_hist = []
visits_grid = np.zeros((10, 10), dtype=int)
uvisited_hist = [np.sum(visits_grid==0)]
def pos_to_grid(pos, grid_size=10):
    """Convert continuous position to discrete grid coordinates."""
    x, y = pos
    grid_x = int((x + 0.5) * grid_size)
    grid_y = int((y + 0.5) * grid_size)
    return (grid_y, grid_x)
robots = []
for i in range(5):
    robot = supervisor.getFromDef(f"EPUCK{i}")
    robots.append(robot)
last_plot_time = 0
while supervisor.step(step) != -1:
    for robot in robots:
        pos = robot.getPosition()
        pos_2d = np.array([pos[0], pos[1]])
        robot_pos_hist.append(pos_2d)
        grid_pos = pos_to_grid(pos_2d)
        visits_grid[grid_pos] += 1
        uvisited_hist.append(np.sum(visits_grid==0))
        if supervisor.getTime() - last_plot_time > 5:
            last_plot_time = supervisor.getTime()
            # pause simulation and plot the positions of the robots
            # plt.figure(figsize=(6, 6))
            # plt.scatter(*zip(*robot_pos_hist), s=1, alpha=0.5)
            # plt.xlim(-0.5, 0.5)
            # plt.ylim(-0.5, 0.5)
            # plt.title(f"Robot positions at time {supervisor.getTime():.2f}s")
            # plt.xlabel("X position (m)")
            # plt.ylabel("Y position (m)")
            # plt.grid()
            
            # heatmap of visits
            # plt.imshow(visits_grid, origin='lower', cmap='hot', interpolation='nearest')
            # plt.colorbar(label='Number of visits')
            # plt.title(f"Heatmap of visits at time {supervisor.getTime():.2f}s")
            # plt.xlabel("Grid X")
            # plt.ylabel("Grid Y")

            # visits over time
            plt.figure(figsize=(6, 4))
            plt.plot(uvisited_hist)
            plt.title(f"Unvisited cells over time")
            plt.xlabel("Time steps")
            plt.ylabel("Unvisited cells")

            # pause the simulation here
            supervisor.simulationSetMode(Supervisor.SIMULATION_MODE_PAUSE)
            plt.show()

            
