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
        zorder= 0,
        color= ("red" if agent.swarm_id == 1 else "blue"),
    )
    return portrayal

MODEL_PARAMS = [10, 10, 15, 9, 9, 0.1, 0.5, 2.0, 2.0, 0.5, 2.0, 2.0] # width, height, num_agents, TARGET_X, TARGET_Y, THRESHOLD, w, C1, C2, w_2, C1_2, C2_2
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
    "TARGET_X": MODEL_PARAMS[3],
    "TARGET_Y": MODEL_PARAMS[4],
    "THRESHOLD": MODEL_PARAMS[5],
    "w": {
        "type": "SliderFloat",
        "value": MODEL_PARAMS[6],
        "label": "w",
        "min": 0.0,
        "max": 1.0,
        "step": 0.1
    },
    "C1": {
        "type": "SliderFloat",
        "value": MODEL_PARAMS[7],
        "label": "C1",
        "min": 0.0,
        "max": 10.0,
        "step": 0.2
    },
    "C2": {
        "type": "SliderFloat",
        "value": MODEL_PARAMS[8],
        "label": "C2",
        "min": 0.0,
        "max": 10.0,
        "step": 0.2
    },
    "w_2": {
        "type": "SliderFloat",
        "value": MODEL_PARAMS[9],
        "label": "w_2", 
        "min": 0.0,
        "max": 1.0,
        "step": 0.1
    },
    "C1_2": {
        "type": "SliderFloat",
        "value": MODEL_PARAMS[10],
        "label": "C1_2",
        "min": 0.0,
        "max": 10.0,
        "step": 0.2
    },
    "C2_2": {
        "type": "SliderFloat",
        "value": MODEL_PARAMS[11],
        "label": "C2_2",
        "min": 0.0,
        "max": 10.0,
        "step": 0.2
    }
}

model = simpleModel(MODEL_PARAMS[0], MODEL_PARAMS[1], MODEL_PARAMS[2], TARGET_X=MODEL_PARAMS[3], TARGET_Y=MODEL_PARAMS[4], THRESHOLD=MODEL_PARAMS[5], w=MODEL_PARAMS[6], C1=MODEL_PARAMS[7], C2=MODEL_PARAMS[8], w_2=MODEL_PARAMS[9], C1_2=MODEL_PARAMS[10], C2_2=MODEL_PARAMS[11])

def post_process_space(ax):
    ax.set_aspect("equal")
    # ax.set_xticks([])
    # ax.set_yticks([])
    ax.set_xlim(0, renderer.space.x_max)
    ax.set_ylim(0, renderer.space.y_max)
    # add grid lines
    ax.set_xticks(np.arange(0, renderer.space.x_max+1, 1), minor=True)
    ax.set_yticks(np.arange(0, renderer.space.y_max+1, 1), minor=True)
    ax.grid(which='minor', color='lightgray', linestyle='-', linewidth=0.5)

renderer = SpaceRenderer(
    model,
    backend="matplotlib",
).setup_agents(agent_portrayal)
renderer.post_process = post_process_space
renderer.draw_agents()
renderer.render()

best_fitness = make_plot_component({"best_fitness_1": "red", "best_fitness_2": "blue"}, backend="matplotlib")

def plot_fitness_contour(model):
    fig, ax = plt.subplots(1, 1, figsize=(4,4))
    ax.contourf(model.contour_data[0], model.contour_data[1], model.contour_data[2], levels=50, cmap='viridis', zorder=0)
    ax.scatter([agent.pos[0] for agent in model.agents_by_type[simpleAgent]], [agent.pos[1] for agent in model.agents_by_type[simpleAgent]], color=['red' if agent.swarm_id == 1 else 'blue' for agent in model.agents_by_type[simpleAgent]], zorder=1)
    ax.set_xlim(0, renderer.space.x_max)
    ax.set_ylim(0, renderer.space.y_max)
    # ax.set_xticks([])
    # ax.set_yticks([])
    plt.tight_layout()
    solara.FigureMatplotlib(fig)
    plt.close(fig)

# page = SolaraViz(
#     model,
#     None,
#     components=[plot_fitness_contour,best_fitness],
#     model_params=model_params,
#     name="Swarm Robotics class - Continuous Space",
# )
page = SolaraViz(
    model,
    renderer,
    components=[best_fitness],
    model_params=model_params,
    name="Swarm Robotics class - Continuous Space",
)
page