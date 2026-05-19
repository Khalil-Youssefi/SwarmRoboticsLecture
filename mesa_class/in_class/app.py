from mesa.visualization import (
    Slider,
    SolaraViz,
    SpaceRenderer,
    make_plot_component,
)
from mesa.visualization.components import AgentPortrayalStyle

from model import simpleModel
from agent import simpleAgent

import numpy as np
import solara
from matplotlib import pyplot as plt

def agent_portrayal(agent):
    if agent is None:
        return
    portrayal = AgentPortrayalStyle(
        size= 50,
        marker= "o",
        color= agent.color,
    )
    return portrayal

model_params = {
    "width": 10,
    "height": 10,
    "num_agents": {
        "type": "SliderInt",
        "value": 5,
        "label": "Number of Agents  ",
        "min": 5,
        "max": 1000.0,
        "step": 5
    }
}

model_ = simpleModel()

renderer = SpaceRenderer(
    model_,
    backend="matplotlib",
).setup_agents(agent_portrayal)
renderer.draw_agents()
renderer.render()

page = SolaraViz(
    model_,
    renderer,
    components=[],
    model_params=model_params,
    name="Swarm Robotics class - Continuous Space",
)
page
