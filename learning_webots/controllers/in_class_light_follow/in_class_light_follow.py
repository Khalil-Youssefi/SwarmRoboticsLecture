from controller import Robot
from math import atan2, sqrt, sin, cos
robot = Robot()
timestep = int(robot.getBasicTimeStep())

motor_left = robot.getDevice('left wheel motor')
motor_right = robot.getDevice('right wheel motor')
motor_left.setPosition(float('inf'))
motor_right.setPosition(float('inf'))

distance_sensors = []
for i in range(8):
    sensor = robot.getDevice('ps' + str(i))
    sensor.enable(timestep)
    distance_sensors.append(sensor)
light_sensors = []
for i in range(8):
    sensor = robot.getDevice('ls' + str(i))
    sensor.enable(timestep)
    light_sensors.append(sensor)
    

# set velocity to 0
motor_left.setVelocity(0)
motor_right.setVelocity(0)
while robot.step(timestep) != -1:
    light_values = [sensor.getValue() for sensor in light_sensors]
    # print("Light sensor values:", end=' ')
    # for i, value in enumerate(light_values):
    #     print(f"ls{i}: {value:.2f}", end=' ')
    # print()  # Print a newline after all light sensor values
    group_left = light_values[4] + light_values[5] + light_values[6] + light_values[7]
    group_right = light_values[0] + light_values[1] + light_values[2] + light_values[3]
    if (group_left - group_right) > 5:
        motor_left.setVelocity(3)
        motor_right.setVelocity(1)
    elif (group_right - group_left) > 5:
        motor_left.setVelocity(1)
        motor_right.setVelocity(3)
    else:
        motor_left.setVelocity(3)
        motor_right.setVelocity(3)
