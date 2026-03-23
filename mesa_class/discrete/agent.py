from mesa.discrete_space import CellAgent
import numpy as np
from cell_agent import cell_agent

class simpleAgent(CellAgent):
    def __init__(self, model, unique_id, cell):
        super().__init__(model)
        self.unique_id = unique_id
        self.cell = cell
        self.v = np.random.rand()

    def step(self):
        # visit any cell that we are currently on
        for obj in self.cell.agents:
            if isinstance(obj, cell_agent):
                obj.visit()
        neighboring_cells = self.cell.get_neighborhood(radius=1, include_center=False)
        # first try to get a cell that has a TileAgent and zero_level_check is False
        good_cells = neighboring_cells.select(
            lambda cell:
            not any(isinstance(obj, simpleAgent) for obj in cell.agents)
        )
        if len(good_cells) > 0:
            new_cell = good_cells.select_random_cell()
            self.cell = new_cell