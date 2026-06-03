from controller import Robot

robot = Robot()
timestep = int(robot.getBasicTimeStep())

motor_left = robot.getDevice('left wheel motor')
motor_right = robot.getDevice('right wheel motor')
motor_left.setPosition(float('inf'))
motor_right.setPosition(float('inf'))

sensor_0 = robot.getDevice('ps0')
sensor_1 = robot.getDevice('ps1')
sensor_0.enable(timestep)
sensor_1.enable(timestep)

while robot.step(timestep) != -1:
    motor_left.setVelocity(4.0)
    motor_right.setVelocity(4.0)
    if sensor_0.getValue() > 80.0 or sensor_1.getValue() > 80.0:
        motor_left.setVelocity(4.0)
        motor_right.setVelocity(-4.0)
        robot.step(1000)