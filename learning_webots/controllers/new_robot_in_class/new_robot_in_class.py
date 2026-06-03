from controller import Robot


robot = Robot()

robot.step(5000)

motor = robot.getDevice('rotational motor')
motor.setPosition(float('inf'))
motor.setVelocity(-9.0)

# timestep = int(robot.getBasicTimeStep())

# while robot.step(timestep) != -1:
#     pass