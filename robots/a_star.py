import numpy as np
from typing import List

from robots.maps import Node, BarrierMap
from robots.setting import MAP_SIZE


class ANode(Node):

    def __init__(self, pos: tuple):
        super(ANode, self).__init__(pos)
        self.g = 0  # 离起点距离
        self.h = 0  # 离终端距离
        self.father = None

    def manha(self, node: Node):
        return np.abs(self.x - node.x) + np.abs(self.y - node.y)

    def set_father_a_node(self, a_node):
        self.father = a_node

    def set_h(self, a_node):
        self.h = self.manha(a_node)


class AStar:

    def __init__(self, start_node: Node, end_node: Node, barrier_map):
        self.start_a_node = ANode(start_node.loc())
        self.end_a_node = ANode(end_node.loc())

        self.start_a_node.set_h(self.end_a_node)

        self.open_list = []
        self.open_list.append(self.start_a_node)
        self.close_list = []
        self.barrier_map = barrier_map

    def get_min_f_a_node(self) -> ANode:
        min_f_a_node = self.open_list[0]
        for a_node in self.open_list:
            if a_node.g + a_node.h <= min_f_a_node.g + min_f_a_node.h:
                min_f_a_node = a_node
        return self.open_list.pop(self.open_list.index(min_f_a_node))

    def process(self) -> ANode:
        while self.open_list:
            current_a_node = self.get_min_f_a_node()
            self.close_list.append(current_a_node)

            if current_a_node.loc() == self.end_a_node.loc():
                return current_a_node

            self.filter_neighbour_nodes(current_a_node)

    def filter_neighbour_nodes(self, a_node: ANode):
        close_a_node_loc = [node.loc() for node in self.close_list]
        open_a_node_loc = [node.loc() for node in self.open_list]
        for i, j in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            nei_loc = (a_node.x + i, a_node.y + j)
            if 0 <= nei_loc[0] < MAP_SIZE[0] and 0 <= nei_loc[1] < MAP_SIZE[1]:
                if self.barrier_map.map[nei_loc[0], nei_loc[1]] or nei_loc in close_a_node_loc:
                    continue
                if nei_loc in open_a_node_loc:
                    nei_open_node = self.open_list.pop(open_a_node_loc.index(nei_loc))
                    if nei_open_node.g + nei_open_node.h <= a_node.g + 1 + nei_open_node.h:
                        nei_open_node.father = a_node
                        nei_open_node.g = a_node.g + 1
                    self.open_list.append(nei_open_node)
                else:
                    nei_node = ANode(nei_loc)
                    nei_node.set_h(self.end_a_node)
                    nei_node.g = a_node.g + 1
                    nei_node.father = a_node
                    self.open_list.append(nei_node)

    def run(self) -> List[Node]:
        a_node = self.process()
        node_list, a_node = [Node(a_node.loc())], a_node.father
        try:
            while a_node.father is not None:
                node_list.append(Node(a_node.loc()))
                a_node = a_node.father
        except AttributeError as e:
            pass

        node_list.reverse()
        return node_list
