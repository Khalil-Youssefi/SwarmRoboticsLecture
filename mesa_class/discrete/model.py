from mesa import Model
from mesa.discrete_space import OrthogonalMooreGrid
from agent import simpleAgent
from cell_agent import cell_agent
import numpy as np

class simpleModel(Model):
    def __init__(self, width, height, num_agents):
        super().__init__()
        self.grid = OrthogonalMooreGrid([width, height], torus=False, capacity=100)
        self.num_agents = num_agents

        self.moving_agents = []
        agents_to_place = self.num_agents
        ids = 0
        while agents_to_place > 0:
            x = np.random.randint(0, width - 1)
            y = np.random.randint(0, height - 1)

            placement_ok = True
            if len(self.grid[x, y].agents) > 0:
                placement_ok = False
            if placement_ok:
                agent = simpleAgent(self, ids, self.grid[x, y])
                self.agents.add(agent)
                self.moving_agents.append(agent)
                ids += 1
                agents_to_place -= 1
        self.fixed_agents = []
        for cell in self.grid:
            cell_agent_instance = cell_agent(self, len(self.agents), cell)
            self.agents.add(cell_agent_instance)
            self.fixed_agents.append(cell_agent_instance)

    def step(self):
        self.agents_by_type[simpleAgent].shuffle().do('step')
        # if self.agents_by_type[cell_agent].agg('visited', lambda x: sum(x)) > 20:
        #     self.running = False
        if self.agents_by_type[cell_agent].agg('visited', all):
            self.running = False