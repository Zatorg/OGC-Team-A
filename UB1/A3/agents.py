from mesa import Agent

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

    def pickup(self, particle):
        p_pick = particle.p_pick()
        if self.random.random() < p_pick:
            particle.free = False
            self.particle = particle
            self.loaded = True

    def pick(self):
        particle = self.model.random_particle()
        self.move_to(particle.pos)
        self.pickup(particle)

    def drop(self):
        p_drop = self.particle.p_drop()
        if self.random.random() < p_drop:
            if not self.model.grid.is_cell_empty(self.pos):
                self.find_empty(radius=1)
            self.particle.free = True
            self.loaded = False
            self.particle = None

    def find_empty(self, radius=None):
        if radius==None: radius = self.model.stepsize
        nbh = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=True, radius=radius)
        free_cells = [cell for cell in nbh if self.model.grid.is_cell_empty(cell)]
        if len(free_cells) > 1:
            new_position = self.random.choice(free_cells)
            self.move_to(new_position)
        else: 
            print("No free cell in neighborhood")

    def initial_step(self):
        particle = self.model.random_particle()

        particle.free = False
        self.particle = particle
        self.loaded = True

        pos = self.model.grid.find_empty()
        self.move_to(pos)

    def step(self):
        self.move(self.model.stepsize)

        if self.loaded:
            self.drop()
            while not self.loaded:
                self.pick()


class Particle(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.free = True

    def move(self, new_position):
        self.model.grid.move_agent(self, new_position)

    def initial_step(self):
        pass

    def step(self):
        pass

    def dissimilarity(self, other):
        return int(type(self) is not type(other))

    def f(self):
        l = []

        others, nbh_size = self.model.grid.get_particles_in_neighborhood(self.pos, moore=True,
                                               include_center=True,
                                               radius=self.model.perception_radius)
        sigma_squared = nbh_size

        for other in others:
            a = (self.dissimilarity(other) / self.model.alpha)
            diss_val = 1-a
            l.append(diss_val)

        if all(i > 0 for i in l):
            val = (1/sigma_squared) * sum(l)
        else:
            val = 0
        return val

    def p_pick(self):
        p = self.model.k_plus / (self.model.k_plus + self.f())
        return p**2

    def p_drop(self):
        p = self.f() / (self.model.k_minus + self.f())
        return p**2


class Stone(Particle):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


class Leaf(Particle):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


class Stick(Particle):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
