from mesa import Model
from mesa.datacollection import DataCollector
import numpy as np

import plotter
import emergence as em
from emergence import entropy_loaded, entropy_neighbors, entropy_xpos_ants, entropy_ypos_ants, entropy_xpos_particles, entropy_ypos_particles
from emergence import emergence_loaded, emergence_neighbors, emergence_xpos_ants, emergence_ypos_ants, emergence_ypos_particles, emergence_xpos_particles

from agents import Ant, Stick, Stone, Leaf
from grid import ClusterGrid
from scheduler import ClusterScheduler


class ClusteringModel(Model):
    def __init__(self, N, density, stepsize, perception_radius,
                 alpha, k_plus, k_minus, random_creation,
                 width=50, height=50):
        self.num_ants = N
        self.density = density
        self.stepsize = stepsize
        self.perception_radius = perception_radius

        self.alpha = alpha
        self.k_plus = k_plus
        self.k_minus = k_minus

        self.random_creation = random_creation

        self.grid = ClusterGrid(width, height, True)
        self.schedule = ClusterScheduler(self)
        self.running = True

        self.create_particles()
        self.create_ants()
        self.schedule.init_agent_lists()
        self.schedule.initial_step()

        self.dc_entropy = DataCollector(
            model_reporters={"X-Pos Ants": em.entropy_xpos_ants,
                             "Y-Pos Ants": em.entropy_ypos_ants,
                             "X-Pos Particles": em.entropy_xpos_particles,
                             "Y-Pos Particles": em.entropy_ypos_particles,
                             "Loaded": em.entropy_loaded,
                             "Neighbors": em.entropy_neighbors}
        )

        self.dc_emergence = DataCollector(
            model_reporters={"X-Pos Ants": em.emergence_xpos_ants,
                             "Y-Pos Ants": em.emergence_ypos_ants,
                             "X-Pos Particles": em.emergence_xpos_particles,
                             "Y-Pos Particles": em.emergence_ypos_particles,
                             "Loaded": em.emergence_loaded,
                             "Neighbors": em.emergence_neighbors}
        )

        self.entropy_t0 = {}

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

            p = P(i + self.num_ants, self)
            pos = (particle_coords[i, 0], particle_coords[i, 1])
            self.schedule.add(p)
            self.grid.place_agent(p, pos)

    def random_particle(self):
        free_particles = [p for p in self.schedule.particle_agents if p.free]
        choice = self.random.randint(0, len(free_particles) - 1)
        return free_particles[choice]

    def step(self):
        if self.schedule.steps == 0:
            self.entropy_t0['xpos_p'] = em.entropy_xpos_particles(self)
            self.entropy_t0['ypos_p'] = em.entropy_ypos_particles(self)
            self.entropy_t0['xpos_a'] = em.entropy_xpos_ants(self)
            self.entropy_t0['ypos_a'] = em.entropy_ypos_ants(self)
            self.entropy_t0['loaded'] = em.entropy_loaded(self)
            self.entropy_t0['neighb'] = em.entropy_neighbors(self)

        self.dc_entropy.collect(self)
        self.dc_emergence.collect(self)
        self.schedule.step()

        # Plot mit matplotlib
        if self.schedule.steps % 200 == 0:
            entropy = self.dc_entropy.get_model_vars_dataframe()
            emergence = self.dc_emergence.get_model_vars_dataframe()

            # save_chart=True saves the charts into charts/t{stepsize}.jpg
            # show_plot=True recommended only for pycharm scientific plots in tool window
            # plotter.plot_([entropy, emergence], step=self.schedule.steps, smooth=True, show_plot=False, save_chart=False)
