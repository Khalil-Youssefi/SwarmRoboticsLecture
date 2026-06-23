from controller import Supervisor

supervisor = Supervisor()
step = int(supervisor.getBasicTimeStep())

# add E-puck by string
epuck_string = "DEF EPUCK1 E-puck { name \"EPUCK1\" translation -0.1 0.1 0.01 rotation 0 0 1 1.14 controller \"in_class_light_follow\" }"
# directly add the E-puck to the scene
supervisor.getRoot().getField("children").importMFNodeFromString(-1, epuck_string)