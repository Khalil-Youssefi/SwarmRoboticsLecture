from mesa.agent import Agent
import numpy as np
class simpleAgent(Agent):
    def __init__(self, model, unique_id):
        super().__init__(model)
        self.unique_id = unique_id
        self.color = np.random.choice(["red", "blue"])

    def step(self):
        another_agent = self.random.choice([a for a in self.model.agents if a.color == self.color])
        velocity = np.array(another_agent.pos) - np.array(self.pos)
        velocity = velocity / np.linalg.norm(velocity) * 0.5
        new_pos = self.pos + velocity
        if new_pos[0] >= 0 and new_pos[0] < self.model.width and new_pos[1] >= 0 and new_pos[1] < self.model.height:
            self.model.space.move_agent(self, new_pos)













