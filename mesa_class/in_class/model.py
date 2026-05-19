from mesa.model import Model
from agent import simpleAgent
import numpy as np
from mesa.space import ContinuousSpace

class simpleModel(Model):
    def __init__(self, width=10, height=10, num_agents=5):
        super().__init__()
        self.num_agents = num_agents
        self.width = width
        self.height = height
        self.space = ContinuousSpace(self.width, self.height, torus=False)

        id = 0
        for i in range(self.num_agents):
            id += 1
            pos = (np.random.rand()*self.width, np.random.rand()*self.height)
            a = simpleAgent(self, id)
            self.space.place_agent(a, pos)
    def step(self):
        self.agents.shuffle().do('step')