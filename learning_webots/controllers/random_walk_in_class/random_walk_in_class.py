from controller import Supervisor
from math import atan2, sqrt, sin, cos
robot = Supervisor()
timestep = int(robot.getBasicTimeStep())

motor_left = robot.getDevice('left wheel motor')
motor_right = robot.getDevice('right wheel motor')
motor_left.setPosition(float('inf'))
motor_right.setPosition(float('inf'))

sensor_0 = robot.getDevice('ps0')
sensor_1 = robot.getDevice('ps1')
sensor_0.enable(timestep)
sensor_1.enable(timestep)

motor_left.setVelocity(0)
motor_right.setVelocity(0)

xt,yt = 0,0
while robot.step(timestep) != -1:
    x = robot.getSelf().getPosition()[0]
    y = robot.getSelf().getPosition()[1]

    orientation = robot.getSelf().getOrientation()
    fw_x = orientation[0]
    fw_y = orientation[3]
    yaw = atan2(fw_y, fw_x)
    # normalize yaw to [0, 2*pi]
    theta = atan2(sin(yaw), cos(yaw))
    
    
    delta_x = xt - x
    delta_y = yt - y

    theta_prime = atan2(delta_y, delta_x)
    theta_prime = atan2(sin(theta_prime), cos(theta_prime))

    delta_theta = theta_prime - theta
    distance = sqrt(delta_x**2 + delta_y**2)

    if distance > 0.01:
        forward_speed = 3
        rotation_speed = 2 * delta_theta
        left_speed = forward_speed - rotation_speed
        right_speed = forward_speed + rotation_speed
        left_speed = max(min(left_speed, 4), -4)
        right_speed = max(min(right_speed, 4), -4)
        motor_left.setVelocity(left_speed)
        motor_right.setVelocity(right_speed)
    else:
        motor_left.setVelocity(0)
        motor_right.setVelocity(0)
