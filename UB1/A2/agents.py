from mesa import Agent

import random
import numpy as np

# TODO Test Changes
class Ant(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.loaded = False
        self.object = None

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
            if type(cellmate) is Object and cellmate is not self.particle:
                return cellmate
        return None

    def pickup(self, object):
        p_pickup = self.model.k_plus / (self.model.k_plus + object.neigbourhood_lumer_faieta())
        if self.random.random() < p_pickup:
            self.object = object
            self.loaded = True
        self.move(self.model.jumpsize)

    # TODO Implement probability based drop
    def drop(self):
        self.loaded = False
        self.object = None
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


class Object(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def move(self, new_position):
        self.model.grid.move_agent(self, new_position)

    def step(self):
        pass

    def distance_object(self, object):
        if type(self) is type(object):
            return 0.0
        else:
            return 1.0

    def neigbourhood_lumer_faieta(self):
        sum = 0.0
        # TODO add viewdistance
        nbh = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=True, radius=self.model.stepsize)
        for cellmate in self.model.grid.get_cell_list_contents(nbh):
            if cellmate.__bases__ is self.__bases__:
                sum += 1.0 - (distance_object(cellmate) / self.model.alpha)
        f = sum / ((2 * (self.model.stepsize - 1) + 1)**2)
        return max(f, 0)


class Stone(Object):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


class Leaf(Object):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


class Stick(Object):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

