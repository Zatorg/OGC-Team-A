from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter


from model import ClusteringModel
from agents import Ant, Stone, Stick, Leaf


def agent_portrayal(agent):
    portrayal = {"Filled": "true"}
    
    if type(agent) is Ant:
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "black"
        portrayal["r"] = 0.8
        portrayal["Layer"] = 0

    elif type(agent) is Stone:
        portrayal["Shape"] = "circle"
        portrayal["Color"] = "#848884"
        portrayal["r"] = 0.5
        portrayal["Layer"] = 1

    elif type(agent) is Leaf:
        portrayal["Shape"] = "arrowHead"
        portrayal["Color"] = "#0BDA51"
        portrayal["scale"] = 0.6
        portrayal["heading_x"] = 1
        portrayal["heading_y"] = 0
        portrayal["Layer"] = 2

    elif type(agent) is Stick:
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


grid = CanvasGrid(agent_portrayal, 50, 50, 700, 700)

entropy_chart = ChartModule(
    [{"Label": "Neighbors", "Color": "Red"},
     {"Label": "X-Pos Particles", "Color": "Green"},
     {"Label": "Y-Pos Particles", "Color": "Green"},
     {"Label": "X-Pos Ants", "Color": "Blue"},
     {"Label": "Y-Pos Ants", "Color": "Blue"},
     {"Label": "Loaded", "Color": "Black"}],
    canvas_height=300,
    data_collector_name='dc_entropy')

emergence_chart = ChartModule(
    [{"Label": "Neighbors", "Color": "Red"},
     {"Label": "X-Pos Particles", "Color": "Green"},
     {"Label": "Y-Pos Particles", "Color": "Green"},
     {"Label": "X-Pos Ants", "Color": "Blue"},
     {"Label": "Y-Pos Ants", "Color": "Blue"},
     {"Label": "Loaded", "Color": "Black"}],
    canvas_height=300,
    data_collector_name='dc_emergence')

arguments = {
    "N": UserSettableParameter("slider", "#Ants", 45, 10, 300),
    "width": 50,
    "height": 50,
    "density": UserSettableParameter("slider", "Particle Density", 0.15, 0.01, 0.5, 0.01),
    "stepsize": UserSettableParameter("slider", "Step Size", 3, 1, 5),
    "perception_radius": UserSettableParameter("slider", "Perception Radius", 2, 1, 5),
    "alpha": UserSettableParameter("slider", "Alpha", 0.5, 0.01, 1.0, 0.01),
    "k_plus": UserSettableParameter("slider", "K+", 0.1, 0.01, 1.0, 0.01),
    "k_minus": UserSettableParameter("slider", "K-", 0.3, 0.01, 1.0, 0.01),
    "random_creation": UserSettableParameter("checkbox", "Random Creation", True),
}

# mit Live-Charts von Mesa:
server = ModularServer(ClusteringModel, [grid, entropy_chart, emergence_chart], "Clustering Model", arguments)

# Ohne Live-Charts
# server = ModularServer(ClusteringModel, [grid], "Clustering Model", arguments)
server.port = 8521
