from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

import model
from model import ClusteringModel

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.7}
    
    if type(agent) is model.Ant:
        portrayal["Color"] = "black"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.3

    return portrayal


grid = CanvasGrid(agent_portrayal, 50, 50, 500, 500)
#chart = ChartModule([{"Label": "Wolfes", "Color": "#A00"}, {"Label":"Sheep", "Color":"#666"}])


arguments = {
    "N": UserSettableParameter("slider", "#Ants", 100, 10, 300),
    "width":50,
    "height":50,
    "density": UserSettableParameter("slider", "Particle Density", 0.1, 0.01, 1.0, 0.01),
    "s": UserSettableParameter("slider", "Step Size", 1, 1, 5),
    "j": UserSettableParameter("slider", "Jump Size", 3, 2, 10),
    "random_creation": UserSettableParameter("checkbox", "Random Creation", True)
}

server = ModularServer(ClusteringModel, [grid], "Clustering Model", arguments)
server.port = 8521
