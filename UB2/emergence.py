import numpy as np
import math


def shannon_entropy(vals, minlength=0):
    ent = 0.0
    if len(vals) < 2:
        return ent

    freq = np.bincount(vals, minlength=minlength)
    size = float(len(vals))

    for f in freq:
        if f > 0:
            p = float(f) / size
            ent += p * math.log(p, 2)

    return -ent


# ANTS
def entropy_xpos_ants(model):
    agents = model.schedule.ant_agents
    positions = [i.pos[0] for i in agents]
    return shannon_entropy(positions)


def entropy_ypos_ants(model):
    agents = model.schedule.ant_agents
    positions = [i.pos[1] for i in agents]
    return shannon_entropy(positions, model.grid.height)


def entropy_loaded(model):
    agents = model.schedule.ant_agents
    ants_loaded = [int(i.loaded) for i in agents]
    return shannon_entropy(ants_loaded, 2)


def emergence_xpos_ants(model):
    return model.entropy_t0['xpos_a'] - entropy_xpos_ants(model)


def emergence_ypos_ants(model):
    return model.entropy_t0['ypos_a'] - entropy_ypos_ants(model)


def emergence_loaded(model):
    return model.entropy_t0['loaded'] - entropy_loaded(model)


# PARTICLES
def entropy_xpos_particles(model):
    agents = model.schedule.particle_agents
    positions = [i.pos[0] for i in agents]
    return shannon_entropy(positions)


def entropy_ypos_particles(model):
    agents = model.schedule.particle_agents
    positions = [i.pos[1] for i in agents]
    return shannon_entropy(positions)


def entropy_neighbors(model):
    particles = model.schedule.particle_agents
    neighbor_counts = [len(model.grid.get_particles_in_neighborhood(p.pos, types=[type(p)]))
                       for p in particles]
    return shannon_entropy(neighbor_counts, minlength=8)


def emergence_xpos_particles(model):
    return model.entropy_t0['xpos_p'] - entropy_xpos_particles(model)


def emergence_ypos_particles(model):
    return model.entropy_t0['ypos_p'] - entropy_ypos_particles(model)


def emergence_neighbors(model):
    return model.entropy_t0['neighb'] - entropy_neighbors(model)
