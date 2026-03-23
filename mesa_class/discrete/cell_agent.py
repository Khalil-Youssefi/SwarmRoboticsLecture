from mesa.discrete_space import FixedAgent

class cell_agent(FixedAgent):
    def __init__(self, model, unique_id, cell):
        super().__init__(model)
        self.unique_id = unique_id
        self.cell = cell
        self.visited = False
        self.visits = 0
    def visit(self):
        self.visited = True
        self.visits += 1