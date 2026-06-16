from controller import Robot, Motor, DistanceSensor, device, distance_sensor
import numpy as np

DISTANCE_SENSORS_NUMBER  = 8
LIGHT_SENSORS_NUMBER = 8
MAX_SPEED = 3

# initialization
robot = Robot()
timestep = int(robot.getBasicTimeStep())
# get devices
distance_sensors = []
for i in range(DISTANCE_SENSORS_NUMBER):
    distance_sensors.append(robot.getDevice('ps' + str(i)))
    distance_sensors[i].enable(timestep)

light_sensors = []
for i in range(DISTANCE_SENSORS_NUMBER):
    light_sensors.append(robot.getDevice('ls' + str(i)))
    light_sensors[i].enable(timestep)

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
    ls_values = []
    for i in range(LIGHT_SENSORS_NUMBER):
        ls_values.append(light_sensors[i].getValue())

    # try to follow the light source
    left_speed = MAX_SPEED
    right_speed = MAX_SPEED
    print(f"Light sensor values: {ls_values}")
    reference_light_value = (ls_values[0] + ls_values[7]) / 2
    right_light_value = np.mean((ls_values[0], ls_values[1], ls_values[2], ls_values[3]))
    left_light_value = np.mean((ls_values[4], ls_values[5], ls_values[6], ls_values[7]))
    THRESHOLD = 0.1 * reference_light_value
    if reference_light_value - left_light_value> THRESHOLD:
        # turn left
        left_speed = -MAX_SPEED
        right_speed = MAX_SPEED
        print(f"Turning left: left_light_value={left_light_value}, reference_light_value={reference_light_value}")
    elif reference_light_value - right_light_value > THRESHOLD:
        # turn right
        left_speed = MAX_SPEED
        right_speed = MAX_SPEED
        print(f"Turning right: right_light_value={right_light_value}, reference_light_value={reference_light_value}")
    else:
        print(f"Going straight: left_light_value={left_light_value}, right_light_value={right_light_value}, reference_light_value={reference_light_value}")
    
    # if any sensor detects an obstacle, EMERGENCY STOP
    if any(value > 100 for value in ps_values[-1:1]):
        left_speed = 0
        right_speed = 0
    
    # set motor speeds
    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)

