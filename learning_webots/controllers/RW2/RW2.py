from controller import Robot, Motor, DistanceSensor, device, distance_sensor
import numpy as np

DISTANCE_SENSORS_NUMBER  = 8
MAX_SPEED = 3

# initialization
robot = Robot()
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


# main loop
while robot.step(timestep) != -1:
    # read sensors
    ps_values = []
    for i in range(DISTANCE_SENSORS_NUMBER):
        ps_values.append(distance_sensors[i].getValue())
    
    # Broaning behavior
    rotation_time = np.random.uniform(0.1, 1)
    walk_time = np.random.uniform(0.1, 1)
    
    # rotate
    if np.random.rand() < 0.5:
        left_motor.setVelocity(MAX_SPEED)
        right_motor.setVelocity(-MAX_SPEED)
    else:
        left_motor.setVelocity(-MAX_SPEED)
        right_motor.setVelocity(MAX_SPEED)
    robot.step(int(rotation_time*1000))

    # walk
    left_motor.setVelocity(MAX_SPEED)
    right_motor.setVelocity(MAX_SPEED)
    robot.step(int(walk_time*1000))
    

