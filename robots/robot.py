import numpy as np
from typing import Union

from robots.setting import (
    BOT_COMMUNICATE_RANGE,
    BOT_MOVING_RANGE,
    PROFIT_RATIO,
    PHE_RATIO,
)

from robots.maps import ExploreMap, PheMap, Node


class Robot:

    def __init__(self, node: Union[Node, tuple]):
        if isinstance(node, Node):
            self.node = node
        elif isinstance(node, tuple):
            self.nod = Node(node)
        else:
            raise TypeError
        self.comm_range = BOT_COMMUNICATE_RANGE
        self.mov_range = BOT_MOVING_RANGE
        self.loc_barrier_map = ExploreMap()
        self.loc_explore_map = ExploreMap()
        self.moving_path = []
        self.explore_node_list = []

    def loc(self) -> tuple:
        return self.node.loc()

    def moving_profit(self, node: Node) -> Union[float, None]:
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
            return None

    def get_manha_distance(self, node: Node) -> int:
        return np.abs(self.node.x - node.x) + np.abs(self.node.y - node.y)

    def get_accessibility(self, node: Node) -> bool:
        if np.sqrt((self.node.x - node.x) ** 2 + (self.node.y - node.y) ** 2) < self.comm_range:
            return True
        else:
            return False

    def get_explore_profit(self) -> int:
        # todo explore profit
        return 1

    def get_phe_level(self, node: Node) -> float:
        phe_map = self.get_global_phe_map()
        return phe_map.get_phe(self.node, node)

    def get_global_phe_map(self) -> PheMap:
        # todo global phemap
        b = PheMap()
        return b

    def is_finished(self):
        return self.loc_explore_map.is_finished()

    def get_await_nodes(self) -> Node:
        pass

    def release_node_and_wait_for_buyer(self):
        pass

    def explore(self, node: Node):
        pass
