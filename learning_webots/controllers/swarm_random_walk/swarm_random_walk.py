from controller import Robot
from math import atan2, sqrt, sin, cos
import numpy as np
robot = Robot()
name = robot.getName()
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
    
MX_SPEED = 4
# set velocity to 0
motor_left.setVelocity(MX_SPEED)
motor_right.setVelocity(MX_SPEED)
while robot.step(timestep) != -1:
    distance_values = [sensor.getValue() for sensor in distance_sensors]
    print(f"Distance values for {name}:", distance_values)
    head_sensors = (distance_values[0] + distance_values[7]) / 2
    other_sensors_min = np.min(distance_values[1:7])
    print(f"{name}: Head sensors: {head_sensors}, other_sensors sensors: {other_sensors_min}, ratio: {other_sensors_min / head_sensors}")
    if other_sensors_min / head_sensors < 0.7:
        motor_left.setVelocity(-MX_SPEED)
        motor_right.setVelocity(MX_SPEED)
        robot.step(timestep * 5)
    else:
        motor_left.setVelocity(MX_SPEED)
        motor_right.setVelocity(MX_SPEED)