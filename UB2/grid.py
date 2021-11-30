from agents import Stone, Leaf, Stick
from mesa.space import MultiGrid


class ClusterGrid(MultiGrid):
    def __init__(self, width, height, torus=False):
        super().__init__(width, height, torus)

    def get_particles_in_neighborhood(self, pos, moore=True, include_center=False, radius=1, types=None):
        if types is None:
            types = [Stone, Leaf, Stick]
        nbh = self.get_neighborhood(pos=pos, moore=moore,
                                    include_center=include_center,
                                    radius=radius)
        particles = []
        for (x, y) in nbh:
            contents = self.grid[x][y]
            if len(contents) > 0:
                particles.extend([c for c in contents if type(c) in types])

        return particles
