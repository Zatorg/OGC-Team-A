from mesa.time import RandomActivation
from mesa import Model
from agents import Ant, Particle


class ClusterScheduler(RandomActivation):
    def __init__(self, model: Model):
        super().__init__(model)
        self.particle_agents = None
        self.ant_agents = None

    def init_agent_lists(self):
        self.particle_agents = [agent for agent in self.agents if type(agent).__bases__[0] is Particle]
        self.ant_agents = [agent for agent in self.agents if type(agent) is Ant]

    def initial_step(self):
        for agent in self.agent_buffer(shuffled=True):
            agent.initial_step()

    def step(self) -> None:
        for agent in self.agent_buffer(shuffled=True):
            agent.step()
        self.steps += 1
        self.time += 1
