from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid, Coordinate
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner

import numpy as np
from agents import Ant, Particle, Stick, Stone, Leaf

'''
def clustercount(grid):
    sum_grid = np.zeros_like(grid)
    maxi, maxj = grid.shape

    for i in range(maxi):
        for j in range(maxj):
            arr_to_sum = grid[max(0, i-1): min(i+2,maxj), max(0, j-1): min(j+2, maxj)]
            sum = np.sum(arr_to_sum)
            sum_grid[i,j] = sum * grid[i, j]

    cluster_grid = sum_grid
    res_grid = None

    while not np.array_equal(cluster_grid, res_grid):
        res_grid = cluster_grid
        for i in range(maxi):
            for j in range(maxj):
                if res_grid[i, j] < 2: continue
                arr = res_grid[max(0, i-1): min(i+2,maxj), max(0, j-1): min(j+2, maxj)]
                if np.max(arr) > res_grid[i, j]:
                    cluster_grid[i, j] = np.max(arr)

    return cluster_grid

def compute_singles(model, thresh=7):
    particle_positions = [agent.pos for key, agent in model.schedule._agents.items() if type(agent) is Particle]
    
    grid = np.zeros((model.grid.width, model.grid.height))
    for i in particle_positions:
        grid[i] += 1

    res = clustercount(grid)
    count_arr = np.bincount(res)
    return np.sum(count_arr[1, thresh])
'''


class ClusteringModel(Model):
    def __init__(self, N, density=0.1, stepsize=1,
                 alpha=0.5, k_plus=0.1, k_minus=0.3,
                 width=50, height=50, random_creation=True):
        self.num_ants = N
        self.density = density
        self.stepsize = stepsize

        self.alpha = alpha
        self.k_plus = k_plus
        self.k_minus = k_minus

        self.random_creation = random_creation

        self.grid = ClusterGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        self.create_particles()
        self.create_ants()
        self.initial_step()

    def create_ants(self):
        for i in range(self.num_ants):
            a = Ant(i, self)
            self.schedule.add(a)

            if self.random_creation:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
            else:
                x = int(self.grid.width / 2)
                y = int(self.grid.height / 2)

            self.grid.place_agent(a, (x, y))

    def create_particles(self):
        rands = np.random.uniform(size=(self.grid.width, self.grid.height))
        particle_coords = np.argwhere(rands < self.density)

        for i in range(len(particle_coords)):
            r = self.random.randint(0, 2)
            if r == 0:
                P = Stone
            elif r == 1:
                P = Stick
            elif r == 2:
                P = Leaf
            else:
                print(r, "ERROR")
                P = Particle

            p = P(i + self.num_ants, self)
            pos = (particle_coords[i, 0], particle_coords[i, 1])
            self.schedule.add(p)
            self.grid.place_agent(p, pos)

    def random_particle(self):
        particles = [agent for key, agent in self.schedule._agents.items()
                     if type(agent).__bases__[0] is Particle and agent.free]
        choice = self.random.randint(0, len(particles) - 1)
        return particles[choice]

    def initial_step(self):
        for key, agent in self.schedule._agents.items():
            agent.initial_step()
        print('{"type":"initial_step"}')        # just for fun

    def step(self):
        # singles = compute_singles(self)
        # print(singles)
        #if self.schedule.steps == 0:
            #self.initial_step()
        self.schedule.step()


class ClusterGrid(MultiGrid):
    def __init__(self, width, height, torus=False):
        super().__init__(width, height, torus)

    # hilfsfunktion wegen index error
    def get_particles_in_neighborhood(self, pos, moore, include_center, radius=1):
        nbh = self.get_neighborhood(pos=pos, moore=moore,
                                    include_center=include_center,
                                    radius=radius)
        particles = []
        for (x, y) in nbh:
            contents = self.grid[x][y]
            if len(contents) > 0:
                particles.append([c for c in contents if type(c) in [Stone, Leaf, Stick]])

        return particles, len(nbh)
