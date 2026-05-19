from controller import Supervisor, Motor, DistanceSensor, device, distance_sensor
import numpy as np

DISTANCE_SENSORS_NUMBER  = 8
MAX_SPEED = 3

# initialization
robot = Supervisor()
self_node = robot.getSelf()
if not self_node:
    print("Error: Could not get the robot node.")
    exit(1)
timestep = int(robot.getBasicTimeStep())
# get devices
distance_sensors = []
for i in range(DISTANCE_SENSORS_NUMBER):
    distance_sensors.append(robot.getDevice('ps' + str(i)))
    distance_sensors[i].enable(timestep)

# get motors
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

target_x = 0.0
target_y = 0.2
# main loop
while robot.step(timestep) != -1:
    left_speed = 0;
    right_speed = 0;

    position = self_node.getPosition()
    orientation = self_node.getOrientation()
    x = position[0]
    y = position[1]
    fw_x = orientation[0]
    fw_y = orientation[3]
    theta = np.atan2(fw_y, fw_x)
    
    dx = target_x - x
    dy = target_y - y

    distance = np.sqrt(dx**2 + dy**2)
    if distance < 0.001:
        left_speed = 0
        right_speed = 0
    else:
        theta_prime = np.arctan2(dy, dx)

        dtheta = theta_prime - theta
        dtheta = np.arctan2(np.sin(dtheta), np.cos(dtheta))

        forward_speed = min(MAX_SPEED, 100*distance)
        turn_speed = 2 * dtheta
        left_speed = forward_speed - turn_speed
        right_speed = forward_speed + turn_speed
        left_speed = max(-MAX_SPEED, min(MAX_SPEED, left_speed))
        right_speed = max(-MAX_SPEED, min(MAX_SPEED, right_speed))
    
    # read sensors
    ps_values = []
    for i in range(DISTANCE_SENSORS_NUMBER):
        ps_values.append(distance_sensors[i].getValue())
    # if any sensor detects an obstacle, EMERGENCY STOP
    if ps_values[0] > 100 or ps_values[7] > 100:
        left_speed = 0
        right_speed = 0
    
    # set motor speeds
    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)

