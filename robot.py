from typing import Tuple

import numpy as np 

from setting import (
    BOT_COMMUNICATE_RANGE,
    BOT_MOVING_RANGE,
    MAP_SIZE,
    PROFIT_RATIO,
    PHE_RATIO,
)

from maps import BarrierMap, ExploreMap, PheMap


class Node:

    def __init__(self, pos: tuple):
        self.x = pos[0]
        self.y = pos[1]


class Robot:

    def __init__(self, pos: tuple):
        if len(pos) != 2:
            raise TypeError
        self.node = Node(pos)
        self.comm_range = BOT_COMMUNICATE_RANGE
        self.mov_range = BOT_MOVING_RANGE
        self.loc_barrier_map = ExploreMap()
        self.loc_explore_map = ExploreMap()
        self.moving_path = []

    def moving_profit(self, node: Node) -> float:
        if self.get_accessibility(node):
            moving_cost = self.get_manha_distance(node)
            phe = self.get_phe_level(node)
            explore_profit = self.get_explore_profit()
            r = np.exp(
                PROFIT_RATIO * explore_profit + (1 - PROFIT_RATIO) * (
                    moving_cost + PHE_RATIO * phe
                )
            )
            return r
        else:
            return 

    def get_manha_distance(self, node: Node) -> int:
        return np.abs(self.node.x - node.x) + np.abs(self.node.y - node.y)

    def get_accessibility(self, node: Node) -> bool:
        if np.sqrt((self.node.x - node.x) ** 2 + (self.node.y -node.y) ** 2) < self.comm_range:
            return True
        else:
            return False

    def get_explore_profit(self) -> int:
        # todo fix explore profit
        return 1

    def get_phe_level(self, node: Node) -> float:
        phe_map = self.get_global_phe_map()
        return phe_map.get_phe(self.node, node)

    def get_global_phe_map(self):
        #todo fix global phemap#
        b = PheMap()
        return b
