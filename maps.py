import numpy as np 

from setting import (
    MAP_SIZE,
    BARRIER_PERCENTAGE,
    PHE_VOLATILIZE_CAP
)

from robot import Node


class Map:
    
    def __init__(self):
        self.map = np.zeros(MAP_SIZE, dtype=int)


class BarrierMap(Map):

    def __init__(self):
        super().__init__()
        self.barrier_num = int(MAP_SIZE[0] * MAP_SIZE [1] * BARRIER_PERCENTAGE)
        self.load_barrier()

    def load_barrier(self):
        choices = np.random.choice(np.arange(MAP_SIZE[0] * MAP_SIZE[1]), size=self.barrier_num, replace=False)
        map_flatten = self.map.flatten()
        for choice in choices:
            map_flatten[choice] = 1
        self.map = map_flatten.reshape(MAP_SIZE)

class ExploreMap(Map):
    
    def __init__(self):
        super().__init__()


class PheMap(Map):

    def __init__(self):
        super().__init__()
        self.map = np.zeros_like(self.map, dtype=float)

    def update_phe(self, node: Node):
        self.map[node.x, node.y] += 1

    def phe_volatilize(self):
        map(self.volatilize, self.map)

    @staticmethod
    def volatilize(phe_level: float) -> float:
        return (1 - PHE_VOLATILIZE_CAP) * phe_level

    def get_phe(self,node1: Node, node2: Node) -> float:
        phe = 0
        x_start, x_end = min(node1.x, node2.x), max(node1.x, node2.x)
        y_start, y_end = min(node1.y, node2.y), max(node1.y, node2.y)
        for i in range(x_start, x_end):
            for j in range(y_start, y_end):
                phe += self.map[i, j]
        
        return phe
