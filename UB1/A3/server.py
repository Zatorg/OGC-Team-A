from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

import model
from model import ClusteringModel

def agent_portrayal(agent):
    portrayal = {"Filled": "true"}
    
    if type(agent) is model.Ant:
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "black"
        portrayal["r"] = 0.8
        portrayal["Layer"] = 0

    elif type(agent) is model.Stone:
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "#848884"
        portrayal["r"] = 0.5
        portrayal["Layer"] = 1

    elif type(agent) is model.Leaf:
        portrayal["Shape"] = "arrowHead"
        portrayal["Color"] = "#0BDA51"
        portrayal["scale"] = 0.6
        portrayal["heading_x"] = 1
        portrayal["heading_y"] = 0
        portrayal["Layer"] = 2

    elif type(agent) is model.Stick:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "#C19A6B"
        portrayal["w"] = 0.9
        portrayal["h"] = 0.2
        portrayal["Layer"] = 3

    else:
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "red"
        portrayal["r"] = 0.9
        portrayal["Layer"] = 1

    return portrayal


grid = CanvasGrid(agent_portrayal, 50, 50, 500, 500)
#chart = ChartModule([{"Label": "Wolfes", "Color": "#A00"}, {"Label":"Sheep", "Color":"#666"}])


arguments = {
    "N": UserSettableParameter("slider", "#Ants", 100, 10, 300),
    "width":50,
    "height":50,
    "density": UserSettableParameter("slider", "Particle Density", 0.1, 0.01, 1.0, 0.01),
    "stepsize": UserSettableParameter("slider", "Step Size", 1, 1, 5),
    "perception_radius": UserSettableParameter("slider", "Perception Radius", 1, 1, 5),
    "alpha": UserSettableParameter("slider", "Alpha", 0.5, 0.01, 1.0, 0.01),
    "k_plus": UserSettableParameter("slider", "K+", 0.1, 0.01, 1.0, 0.01),
    "k_minus": UserSettableParameter("slider", "K-", 0.3, 0.01, 1.0, 0.01),
    "random_creation": UserSettableParameter("checkbox", "Random Creation", True)
}

server = ModularServer(ClusteringModel, [grid], "Clustering Model", arguments)
server.port = 8521
