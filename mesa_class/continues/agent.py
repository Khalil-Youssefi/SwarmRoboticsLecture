from mesa import Agent
import numpy as np
from fitness import fitness
class simpleAgent(Agent):
    def __init__(self, model, unique_id, pos, swarm_id=1):
        super().__init__(model)
        self.unique_id = unique_id
        self.pos = pos
        self.swarm_id = swarm_id
        self.v = np.random.rand()
        self.pbest = np.array(self.pos)
        self.pbest_fitness = fitness(self.pbest[0], self.pbest[1], self.model.TARGET_X, self.model.TARGET_Y)
        if self.swarm_id == 1:
            self.w, self.C1, self.C2 = self.model.w, self.model.C1, self.model.C2
        else:
            self.w, self.C1, self.C2 = self.model.w_2, self.model.C1_2, self.model.C2_2
    def step(self):
        current_fitness = fitness(self.pos[0], self.pos[1], self.model.TARGET_X, self.model.TARGET_Y)
        if current_fitness < self.pbest_fitness:
            self.pbest = np.array(self.pos)
            self.pbest_fitness = current_fitness
        gbest = self.pbest
        gbest_fitness = self.pbest_fitness
        for agent in self.model.agents:
            if isinstance(agent, simpleAgent) and agent.swarm_id == self.swarm_id and agent.pbest_fitness < gbest_fitness:
                gbest = agent.pbest
                gbest_fitness = agent.pbest_fitness
        r1 = np.random.rand()
        r2 = np.random.rand()
        pos = np.array(self.pos)
        self.v = self.w * self.v + self.C1 * r1 * (self.pbest - pos) + self.C2 * r2 * (gbest - pos)
        v_norm = np.linalg.norm(self.v)
        if v_norm > 2:
            self.v = self.v / np.linalg.norm(self.v) * 0.1
        new_pos = self.pos + self.v
        new_x = max(0, min(self.model.space.x_max-1, new_pos[0]))
        new_y = max(0, min(self.model.space.y_max-1, new_pos[1]))
        self.model.space.move_agent(self, (new_x, new_y))