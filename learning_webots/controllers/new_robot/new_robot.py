from controller import Robot

robot = Robot()

timestep = int(robot.getBasicTimeStep())

motor = robot.getDevice('rotational motor')
motor.setPosition(float('inf'))
while robot.step(timestep) != -1:
    pass