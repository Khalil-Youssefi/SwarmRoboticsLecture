from controller import Robot
from math import atan2, sqrt, sin, cos
import numpy as np
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
    reference_light_value = (light_values[0] + light_values[7])/2
    THRESHOLD = np.mean(light_values) * 0.05
    left_avg = sum(light_values[4:7]) / 4
    right_avg = sum(light_values[1:4]) / 4
    print("Light values:", light_values)
    print("Reference light value:", reference_light_value, "Left average:", left_avg, "Right average:", right_avg)
    if (left_avg - reference_light_value) > THRESHOLD and (right_avg - reference_light_value) > THRESHOLD:
        motor_left.setVelocity(3)
        motor_right.setVelocity(3)
        print("Moving forward")
    else:
        if left_avg - reference_light_value < THRESHOLD:
            motor_left.setVelocity(-3)
            motor_right.setVelocity(3)
            robot.step(10*timestep)
            print("Turning left")
        else:
            motor_left.setVelocity(3)
            motor_right.setVelocity(-3)
            robot.step(10*timestep)
            print("Turning right")
