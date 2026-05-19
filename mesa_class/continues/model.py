from mesa import DataCollector, Model
from mesa.space import ContinuousSpace
from agent import simpleAgent
import numpy as np
from fitness import fitness
class simpleModel(Model):
    def sum_distances(self):
        total_distance = 0
        agents_in_swarm_1 = self.agents_by_type[simpleAgent].select(lambda a: a.swarm_id == 1)
        for agent_i in agents_in_swarm_1:
            for agent_j in agents_in_swarm_1:
                if agent_i != agent_j:
                    total_distance += np.linalg.norm(np.array(agent_i.pos) - np.array(agent_j.pos))
        agents_in_swarm_2 = self.agents_by_type[simpleAgent].select(lambda a: a.swarm_id == 2)
        for agent_i in agents_in_swarm_2:
            for agent_j in agents_in_swarm_2:
                if agent_i != agent_j:
                    total_distance += np.linalg.norm(np.array(agent_i.pos) - np.array(agent_j.pos))
        return total_distance
    def __init__(self, width, height, num_agents, TARGET_X=5, TARGET_Y=5, THRESHOLD=0.1, w=0.5, C1=2.0, C2=2.0, w_2=0.5, C1_2=2.0, C2_2=2.0, rng = None):
        super().__init__()
        if rng is not None:
            self.random = rng
        self.space = ContinuousSpace(x_max=width, y_max=height, torus=False)
        self.num_agents = num_agents
        self.TARGET_X = TARGET_X
        self.TARGET_Y = TARGET_Y
        self.THRESHOLD = THRESHOLD
        self.w = w
        self.C1 = C1
        self.C2 = C2
        self.w_2 = w_2
        self.C1_2 = C1_2
        self.C2_2 = C2_2
        agents_to_place = self.num_agents * 2
        swarm1_agents = self.num_agents
        ids = 0
        swarm_id = 1
        while agents_to_place > 0:
            x = 1 + np.random.random() * (width/2 - 2)
            y = 1 + np.random.random() * (height/2 - 2)
            nearby_agents = []
            # if agents_to_place < self.num_agents:
            #     nearby_agents = self.space.get_neighbors((x, y), radius=1)
            if len(nearby_agents) == 0:
                agent = simpleAgent(self, ids, (x, y), swarm_id)
                self.agents.add(agent)
                self.space.place_agent(agent, (x, y))
                ids += 1
                agents_to_place -= 1
                if swarm1_agents > 0:
                    swarm1_agents -= 1
                else:
                    swarm_id = 2
        self.datacollector = DataCollector(
            model_reporters={"distance_sum": lambda m: m.sum_distances()}
        )
        self.make_fitness_cotour()
    
    def best_fitness(self, swarm_id=1):
        max_fitness = float('inf')
        for agent in self.agents:
            if isinstance(agent, simpleAgent) and agent.swarm_id == swarm_id and agent.pbest_fitness < max_fitness:
                max_fitness = agent.pbest_fitness
        return max_fitness

    def step(self):
        self.agents_by_type[simpleAgent].shuffle().do('step')
        self.datacollector.collect(self)  # Collect data after agents have moved
        if self.best_fitness(swarm_id=1) < self.THRESHOLD:
            print("Best answer found: ", self.best_fitness(swarm_id=1))
            self.running = False
    def make_fitness_cotour(self):
        x = np.linspace(0, self.space.x_max, 100)
        y = np.linspace(0, self.space.y_max, 100)
        X, Y = np.meshgrid(x, y)
        Z = fitness(X, Y, self.TARGET_X, self.TARGET_Y)
        self.contour_data = [X, Y, Z]