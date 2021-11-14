from mesa import Agent

import random
import numpy as np

class Ant(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.loaded = False
        self.particle = None

    def move_to(self, new_pos):
        self.model.grid.move_agent(self, new_pos)
        if self.loaded:
            self.particle.move(new_pos)
 
    def move(self, steps):
        possible_steps = self.model.grid.get_neighborhood( self.pos, moore=True, include_center=False, radius=steps)
        if steps > 1:
            inner = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False, radius=steps-1)
            possible_steps = [i for i in possible_steps if i not in inner] 

        new_position = self.random.choice(possible_steps)
        self.move_to(new_position)       

    def occupant(self):
        for cellmate in self.model.grid.get_cell_list_contents([self.pos]):
            if type(cellmate) is Particle and cellmate is not self.particle:
                return cellmate
        return None

    def pickup(self, particle):
        self.particle = particle
        self.loaded = True
        self.move(self.model.jumpsize)

    def drop(self):
        self.loaded = False
        self.particle = None
        self.move(self.model.jumpsize)

    def find_empty(self):
        nbh = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False, radius=self.model.stepsize)
        free_cells = [cell for cell in nbh if self.model.grid.is_cell_empty(cell)]
        if len(free_cells) > 1:
            new_position = self.random.choice(free_cells)
            self.move_to(new_position)
        else: 
            print("No free cell in neighborhood")

    def step(self):
        o = self.occupant()

        if o is not None:
            if not self.loaded:
                self.pickup(o)
            else:
                self.find_empty()
                self.drop()
        else:
            self.move(self.model.stepsize)


class Particle(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def move(self, new_position):
        self.model.grid.move_agent(self, new_position)

    def step(self):
        pass

