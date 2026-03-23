from mesa.visualization import (
    Slider,
    SolaraViz,
    SpaceRenderer,
    make_plot_component,
)
from mesa.visualization.components import AgentPortrayalStyle

from model import simpleModel
from agent import simpleAgent
from cell_agent import cell_agent

import numpy as np

def agent_portrayal(agent):
    if agent is None:
        return
    portrayal = AgentPortrayalStyle(
        size= (50 if isinstance(agent, simpleAgent) else 200),
        marker= ("o" if isinstance(agent, simpleAgent) else "s"),
        zorder= (1 if isinstance(agent, simpleAgent) else 0),
        color= ("red" if isinstance(agent, simpleAgent) else ("green" if agent.visited else "lightgreen")),
    )
    return portrayal

MODEL_PARAMS = [10, 10, 5]
model_params = {
    "width": {
        "type": "SliderInt",
        "value": MODEL_PARAMS[0],
        "label": "Grid Width",
        "min": 5,
        "max": 20,
        "step": 1
    },
    "height": {
        "type": "SliderInt",
        "value": MODEL_PARAMS[1],
        "label": "Grid Height",
        "min": 5,
        "max": 20,
        "step": 1
    },
    "num_agents": {
        "type": "SliderInt",
        "value": MODEL_PARAMS[2],
        "label": "Number of Agents",
        "min": 1,
        "max": 20,
        "step": 1
    },
}

model = simpleModel(MODEL_PARAMS[0], MODEL_PARAMS[1], MODEL_PARAMS[2])

def post_process_space(ax):
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    width = renderer.space.width
    height = renderer.space.height
    ax.set_xticks(np.arange(-0.5, width, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, height, 1), minor=True)
    ax.grid(which="minor", color="gray", linestyle=":", linewidth=0.5)

renderer = SpaceRenderer(
    model,
    backend="matplotlib",
).setup_agents(agent_portrayal)
renderer.post_process = post_process_space
renderer.draw_agents()
renderer.render()

page = SolaraViz(
    model,
    renderer,
    components=[],
    model_params=model_params,
    name="Swarm Robotics class - Discrete Space",
)
page