import numpy as np
from abc import ABC
from typing import List

from robots.setting import (
    MAP_SIZE,
    BARRIER_PERCENTAGE,
    PHE_VOLATILIZE_CAP,
    MAP_EXPLORE_PERCENT,
    ENABLE_PHE,
)


class Node:

    def __init__(self, pos: tuple):
        self.x = pos[0]
        self.y = pos[1]

    def loc(self) -> tuple:
        return self.x, self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Map(ABC):

    def __init__(self):
        self.map = np.zeros(MAP_SIZE, dtype=int)

    def __getitem__(self, indices):
        return self.map[indices[0], indices[1]]


class BarrierMap(Map):

    def __init__(self):
        super(BarrierMap, self).__init__()
        self.barrier_num = int(MAP_SIZE[0] * MAP_SIZE[1] * BARRIER_PERCENTAGE)
        self.load_barrier()

    def load_barrier(self):
        choices = np.random.choice(np.arange(MAP_SIZE[0] * MAP_SIZE[1]), size=self.barrier_num, replace=False)
        map_flatten = self.map.flatten()
        for choice in choices:
            map_flatten[choice] = 1
        self.map = map_flatten.reshape(MAP_SIZE)

    def __call__(self, node: Node) -> bool:
        return self.map[node.x, node.y] == 1

    def get_random_node(self):
        x, y = np.random.choice(range(self.map.shape[0])), np.random.choice(range(self.map.shape[1]))
        while self.map[x, y] == 1:
            x, y = np.random.choice(range(self.map.shape[0])), np.random.choice(range(self.map.shape[1]))
        return Node((x, y))


class ExploreMap(Map):

    def __init__(self):
        super(ExploreMap, self).__init__()

    def update(self, node: Node):
        self.map[node.x, node.y] = 1

    def is_finished(self) -> bool:
        if self.map.sum() >= MAP_EXPLORE_PERCENT * self.map.shape[0] * self.map.shape[1]:
            return True
        else:
            return False

    def status(self, node: Node) -> int:
        return self.map[node.loc()]

    def get_neighbours(self, node: Node) -> List:
        node_list = []
        for i, j in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            if node.x - i < 0 or node.x + i >= MAP_SIZE[0] \
                    or node.y - j < 0 or node.y + j >= MAP_SIZE[1]:
                continue
            if not self.status(Node((node.x + i, node.y + j))):
                node_list.append(Node((node.x + i, node.y + j)))
        return node_list


class PheMap(Map):

    def __init__(self):
        super(PheMap, self).__init__()
        self.map = np.zeros_like(self.map, dtype=float)

    def update_phe(self, node: Node):
        self.map[node.x, node.y] += ENABLE_PHE

    def phe_volatilize(self):
        map(self.volatilize, self.map)

    @staticmethod
    def volatilize(phe_level: float) -> float:
        return (1 - PHE_VOLATILIZE_CAP) * phe_level

    def get_phe(self, node1: Node, node2: Node) -> float:
        phe = 0
        x_start, x_end = min(node1.x, node2.x), max(node1.x, node2.x)
        y_start, y_end = min(node1.y, node2.y), max(node1.y, node2.y)
        for i in range(x_start, x_end):
            for j in range(y_start, y_end):
                phe += self.map[i, j]

        return phe
